import re
import os
import jieba
import pandas as pd
from tqdm import tqdm
from datetime import datetime
from collections import Counter
from pyecharts.charts import Geo
from matplotlib import pyplot as plt
from pyecharts import options as opts
from pyecharts.globals import GeoType

def read_data(file_name):
    '''
    Read weibo texts and remove duplicates.
    '''
    df = pd.read_csv(file_name, sep='\t', encoding='utf-8')   # 以制表符为列与列之间的分隔
    return df.drop_duplicates()  #去重后剩余27w+行数据

def load_words(root):
    '''
    Load words for jieba dictionary,  
    mark the emotion of each word and
    generate stop-word list.
    '''
    file_names = os.listdir(root)  #获取绝对路径下文件目录
    sent_dict = []
    wordset = set()
    for file_name in file_names:
        position = root + '\\' + file_name  #带有路径的文件名
        jieba.load_userdict(position)  #将词语加入jieba的分词词典
        with open(position, 'r', encoding='utf-8') as f:
            if file_name != 'stopwords_list.txt':
                with open(position, 'r', encoding='utf-8') as f:
                    for word in f:
                        word = word.strip()
                        sent_dict.append((word, file_name[:-4]))  #去掉'.txt'扩展名, 只用文件名
            else:
                for line in f:
                    line = line.rstrip('\n')
                    if len(line):
                        wordset.add(line)
    sent_dict = dict(sent_dict)
    return sent_dict, wordset

def clean_segment(text_list):
    '''
    clean text(url, emoji, @ etc.) and segment words.
    '''
    seg_list = []
    for text in tqdm(text_list):
        text = re.sub(r'(回复)?(//)?\s*@\S*?\s*(:| |$)', ' ', text)     # 去除正文中的@和回复/转发中的用户名
        text = re.sub(r'\[\S+\]', '', text)     # 去除表情符号
        text = re.sub('http\S+', '', text)       # 去除网址
        text = text.replace("转发微博", '')       # 去除无意义的词语
        text = text.replace('我在:', '')
        text = re.sub(r'\s+', ' ', text)    # 合并正文中过多的空格
        cur_seg_list = []
        for word in jieba.lcut(text):  #分词并过滤停用词
            if word not in stop_words:
                cur_seg_list.append(word)
        seg_list.append(cur_seg_list)
    return seg_list

def get_key(dct, value):
    '''
    Get the specific key of the dictionary based on known value.
    '''
    return list(filter(lambda k: dct[k] == value, dct))

def mark_emotion_of_text():
    '''
    Count the number of words of each emotion in each text 
    and mark the emotion(maybe more than one).
    '''
    emotion_of_text = []
    for i in range(len(seg_list)):
        counts = {}
        text = seg_list[i]
        for word in text:
            if word in sent_dict:
                counts[sent_dict[word]] = counts.get(sent_dict[word], 0) + 1
        if sum(counts.values()) == 0:  #如果没有出现情绪词就认为没有情绪
            emotion_of_text.append([])
        else:
            emotion_of_text.append(get_key(counts, max(counts.values())))  #将出现次数最多的情绪作为该文本的情绪(可能不止一个)
    return emotion_of_text

def transform_time_list(weibo_create_time):
    '''
    Transform time format to yyyy-mm-dd hh:mm:ss
    '''
    time_list = []
    for time_stamp in weibo_create_time:
        if type(time_stamp) != str: #特判解决数据中某一行时间缺失的问题
            print(time_stamp)
            time_list.append(None)
        else:
            time_format = datetime.strptime(time_stamp, '%a %b %d %H:%M:%S %z %Y')  #转化时间格式
            time_list.append(time_format)
    return time_list

def is_float_num(str):
    '''
    Judge whether str is a float.
    '''
    s=str.split('.')
    if len(s)>2:
        return False
    else:
        for si in s:
            if not si.isdigit():
                return False
        return True

def transform_space_list(location):
    '''
    Transform string to float.
    '''
    space_list = []
    for pos in location:
        x = pos.find(',')
        if is_float_num(pos[1:x]) and is_float_num(pos[x + 2:-1]):  #特判解决数据中某一行经纬度格式的问题
            space = [float(pos[1:x]), float(pos[x + 2:-1])]
            space_list.append(space)
        else:
            space_list.append(None)
    return space_list

def analyze_time_mode(time_list, emotion, interval):
    '''
    Draw distribution diagram corresponding to given time interval.
    '''
    emotion_time = []
    for i in tqdm(range(len(seg_list))):
        if emotion in emotion_of_text[i]:
            emotion_time.append(time_list[i])
    if interval == 'week':  #周模式(周一至周日的情绪数量分布)
        emo = []
        for i in range(len(emotion_time)):
            if emotion_time[i] != None:
                emo.append(emotion_time[i].weekday())
        counts = Counter(emo)
        weekday = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        plt.bar([weekday[id] for id in counts.keys()], counts.values())  #条形图
        plt.show()
    
def analyze_space_mode(space_list, emotion):
    '''
    Draw maps corresponding to given emotion.
    '''
    special_spot = []
    data = []
    emo = {'sadness':5, 'joy':35, 'fear':65, 'disgust':85, 'anger':100}
    for i in range(len(seg_list)):
        if emotion in emotion_of_text[i]:
            special_spot.append(i)
    geo = Geo()
    geo.add_schema(maptype='china')  #中国地图
    for i in special_spot:
        if space_list[i] != None:
            data.append((emotion + str(i), emo[emotion]))  #构建数据对(名称+数值)
            geo.add_coordinate(name=emotion + str(i), latitude=space_list[i][0], longitude=space_list[i][1])
    geo.add('geo', data, type_=GeoType.EFFECT_SCATTER, symbol_size=5)
    geo.set_series_opts(label_opts=opts.LabelOpts(is_show=False))
    geo.set_global_opts(visualmap_opts=opts.VisualMapOpts(), title_opts=opts.TitleOpts(title='情绪' + emotion + '分布'))
    geo.render('情绪.html')  #生成网页

if __name__ == '__main__':
    df_text = read_data('E:\\BUAA\\大三上\\程设\\week3\\weibo.txt')
    emotions = ['anger', 'disgust', 'joy', 'sadness', 'fear']
    sent_dict, stop_words = load_words('E:\\BUAA\\大三上\\程设\\week3\\emotion_lexicon')

    seg_list = clean_segment(list(df_text['text']))
    emotion_of_text = mark_emotion_of_text()
    time_list = transform_time_list(list(df_text['weibo_created_at']))
    space_list = transform_space_list(list(df_text['location']))
    analyze_time_mode(time_list, 'joy', 'week')
    analyze_space_mode(space_list, 'joy')