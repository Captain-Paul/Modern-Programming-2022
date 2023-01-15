import os
import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pyecharts.charts import Geo
from pyecharts.globals import GeoType
from pyecharts import options as opts

class NotNumError(ValueError):
    def __init__(self, type, region, date, *args):
        if type == 'emission':  #排放量处有空值
            self._message = f'There is nan in the data of {region} at {date} about {args[0]}'
        elif type == 'time':  #时间有空值
            self._message = f'There is nan in the data of {region} at {date} about time'
    
    @property
    def message(self):
        return self._message

class DataAnalysis:
    '''
    Provide data initialization and basic analysis on time and space.
    '''
    def __init__(self):
        self._df_list = {}
        self._time_list = []

    def load_data(self, file_path):
        '''
        Load data of emissions from file_path.
        '''
        file_dir = os.listdir(file_path)
        for file_name in file_dir:
            file = file_path + '\\' + file_name
            df = pd.read_csv(file, encoding='utf-8')
            df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])  #将年月日小时合并为时间
            df = df.drop(['year', 'month', 'day', 'hour'], axis=1)  #删去年月日小时列
            region = file_name[10:-22]  #截取地点名称
            self._df_list[region] = df
            self._time_list = list(df.astype({'date':str})['date'])

        #检查有无空值        
        for region in self._df_list:
            df = self._df_list[region]
            rows_with_na = df[df.isnull().T.any()]
            for index, row in rows_with_na.iterrows():
                for col in df:
                    if pd.isnull(row[col]):
                        if col == 'date':
                            ##自动填充缺失时间并抛出异常(此处抛出异常可有可无)
                            self._df_list[region].loc[index, 'date'] = df.loc[index-1, 'date'] + datetime.timedelta(hours=1)
                            raise NotNumError('time', region, self._df_list[region].loc[index, 'date'])
                        else:
                            ##抛出非时间列的空值异常(考虑用上一行数据或者该时间点的均值数据进行填充)
                            self._df_list[region].loc[index, col] = df.loc[index-1, col]
                            raise NotNumError('emission', region, row['date'], col)

    def query(self, region, emission_type, askdate, hour):
        df = self._df_list[region]
        asktime = '{} {:0>2d}:00:00'.format(askdate, hour)
        return df.loc[self._time_list.index(asktime), emission_type]

    def time_analysis(self, region, emission_type, st_date, st_h, ed_date, ed_h):
        '''
        Changes in the emission of the specific point over time.
        '''
        df = self._df_list[region]
        start_time = '{} {:0>2d}:00:00'.format(st_date, st_h)
        end_time = '{} {:0>2d}:00:00'.format(ed_date, ed_h)
        df_date = df['date'][self._time_list.index(start_time) : self._time_list.index(end_time) + 1]
        df_emission = df[emission_type][self._time_list.index(start_time) : self._time_list.index(end_time) + 1]
        return {time:data for time, data in zip(df_date, df_emission)}      

    def space_analysis(self, emission_type, type='point', *args):  #默认按时间点分析
        '''
        The spatial distribution of emissions at a certain time point or in a period of time.
        type == point args[0]: date; args[1]: hour
        type == period args[0]: start date; args[1]: start hour; args[2]: end date; args[3]: end hour
        '''
        space_dict = {}
        if type == 'point':
            asktime = '{} {:0>2d}:00:00'.format(args[0], args[1])
            for region in self._df_list:
                df = self._df_list[region]
                space_dict[region] = df.loc[self._time_list.index(asktime), emission_type]
        elif type == 'period':
            start_time = '{} {:0>2d}:00:00'.format(args[0], args[1])
            end_time = '{} {:0>2d}:00:00'.format(args[2], args[3])
            for region in self._df_list:
                df = self._df_list[region][self._time_list.index(start_time) : self._time_list.index(end_time) + 1]
                data = np.nanmean(np.array(df[emission_type]))  #用均值表示时间段内的污染物排放量
                space_dict[region] = data
        return space_dict

class Visualization:
    def __init__(self, fig_size):
        plt.rcParams['font.sans-serif'] = ['SimHei']
        plt.rcParams['axes.unicode_minus'] = False
        plt.figure(figsize=fig_size)

    def plot_time_mode(self, region, emission_type, time_dict):
        plt.plot(list(time_dict.keys()), list(time_dict.values()))
        plt.title(region + emission_type + '排放量随时间变化图')
        plt.show()

    def bar_space_mode(self, emission_type, space_dict):
        plt.bar(list(space_dict.keys()), list(space_dict.values()))
        plt.xticks(rotation=30)
        plt.title(emission_type + '的空间分布')
        plt.show()

    def draw_map(self, emission_type, space_dict):
        coordinate_list=[[116.40,39.99], [116.23,40.22], [116.23,40.29],
                        [116.42,39.92], [116.36,39.94], [116.18,39.91],
                        [116.58,40.33], [116.47,39.94], [116.67,40.16],
                        [116.41,39.88], [116.30,39.97], [116.37,39.88]]
        coordinate_dict = dict(zip(list(space_dict.keys()), coordinate_list))
        g = Geo()
        g.add_schema(maptype='北京')
        datapair = []
        for region in space_dict:
            datapair.append((region, space_dict[region]))
            g.add_coordinate(region, coordinate_dict[region][0], coordinate_dict[region][1])
        g.add('Beijing', data_pair=datapair, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
        pieces = [
            {'min': 0, 'max': 35, 'label': '优', 'color': '#3700A4'},
            {'min': 36, 'max': 75, 'label': '良', 'color': '#81AE9F'},
            {'min': 76, 'max': 115, 'label': '轻度污染', 'color': '#E2C568'},
            {'min': 116, 'max': 150, 'label': '中度污染', 'color': '#FCF84D'},
            {'min': 151, 'max': 250, 'label': '重度污染', 'color': '#DD0200'}
        ]
        g.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
        g.set_global_opts(visualmap_opts=opts.VisualMapOpts(is_piecewise=True, pieces=pieces), 
                        title_opts=opts.TitleOpts(title=emission_type + '空间分布'))
        g.render(emission_type + '空间分布.html')

def main():
    data = DataAnalysis()

    try:
        data.load_data('E:\\BUAA\\大三上\\程设\\week7\\PRSA_Data_20130301-20170228')
    except NotNumError as nne:
        print(nne.message)

    print(data.query('Aotizhongxin', 'PM10', '2013-05-01', 3))
    time_dict = data.time_analysis('Huairou', 'PM10', '2014-05-01', 0, '2014-05-03', 0)
    # space_dict = data.space_analysis('PM2.5', 'period', '2015-05-01', 0, '2015-05-31', 23)
    data_view = Visualization((8, 8))
    data_view.plot_time_mode('Huairou', 'PM10', time_dict)
    # data_view.bar_space_mode('PM2.5', space_dict)
    # data_view.draw_map('PM2.5', space_dict)

if __name__ == '__main__': main()