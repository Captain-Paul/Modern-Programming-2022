import os
import abc
import cv2
import jieba
import librosa
import wordcloud
import numpy as np
import pandas as pd
from PIL import Image
from librosa import display
import imageio.v2 as imageio
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer

plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

#适配器抽象类
class Plotter(metaclass=abc.ABCMeta):
    def __init__(self, data):
        self._data = data
    
    @abc.abstractclassmethod
    def plot(self):
        pass

class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y
    
    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

class PointPlotter(Plotter):    
    def plot(self, type='scatter'):
        plt.figure(figsize=(8, 6))
        x = [point.x for point in self._data]
        y = [point.y for point in self._data]
        if type == 'scatter':   #散点图
            plt.scatter(x, y)
        elif type == 'line':  #折线图
            plt.plot(x, y)
        plt.show()

class ArrayPlotter(Plotter):
    def plot(self, type='scatter'):
        fig = plt.figure(figsize=(8, 6))
        if self._data.shape[0] == 2:   #二维
            if type == 'scatter':
                plt.scatter(self._data[:, 0], self._data[:, 1])
            elif type == 'line':
                plt.plot(self._data[:, 0], self._data[:, 1])
        elif self._data.shape[0] == 3:  #三维
            ax = fig.add_subplot(111, projection='3d')
            if type == 'scatter':
                ax.scatter(self._data[0], self._data[1], self._data[2])
            elif type == 'line':
                ax.plot(self._data[0], self._data[1], self._data[2])
        plt.show()

class TextPlotter(Plotter):
    def plot(self, n):
        document = []
        for text in self._data:
            seg_list = jieba.lcut(text)
            document.append(' '.join(seg_list))

        vectorizer = TfidfVectorizer()   #用TF-IDF指标选择关键词
        X = vectorizer.fit_transform(document)
        df = pd.DataFrame({'word': vectorizer.get_feature_names_out(), 
                        'tf-idf': X.toarray().sum(axis=0).tolist()})
        df.sort_values(by='tf-idf', ascending=False)

        wordpng = wordcloud.WordCloud(background_color='white', height=700, width=1000, font_path='C:\Windows\Fonts\simHei.ttf')
        wordpng.generate(" ".join(list(df['word'])[:n]))
        wordpng.to_file('wordcloud.png')        

class ImagePlotter(Plotter):
    def load_image(self, img_path):
        return Image.open(img_path)

    def plot(self, num_row, num_col, fig_size):
        plt.figure(figsize=fig_size)
        file_names = os.listdir(self._data)
        for i in range(len(file_names)):
            img = self.load_image(self._data + '\\' + file_names[i])
            plt.subplot(num_row, num_col, i + 1)
            plt.imshow(img)
            plt.xticks([])
            plt.yticks([])
        plt.show()

class GifPlotter(Plotter):
    def plot(self, type='path'):
        if type == 'path':
            file_names = os.listdir(self._data)
            frame = []
            for file_name in file_names:
                img = imageio.imread(self._data + '\\' + file_name)
                frame.append(img)
            imageio.mimsave('my.gif', frame, 'GIF', duration=0.6)
        elif type == 'list':
            imageio.mimsave('my2.gif', self._data, 'GIF', fps=60)

class KeyFeaturePlotter(Plotter):
    def plot(self):
        pca = PCA(n_components=2)
        pca.fit(self._data)
        new_data = pca.fit_transform(self._data)
        
        plt.scatter(new_data[:, 0], new_data[:, 1])
        plt.show()

class MusicPlotter(Plotter):
    def plot(self):
        y, sr = librosa.load(self._data, duration=10)

        plt.subplot(3, 1, 1)
        display.waveshow(y, sr=sr)  #波形图

        D = librosa.amplitude_to_db(np.abs(librosa.stft(y)), ref=np.max)

        plt.subplot(3, 1, 2)
        display.specshow(D, y_axis='linear')
        plt.colorbar(format='%+2.0f dB')
        plt.title('线性频率功率谱')

        plt.subplot(3, 1, 3)
        display.specshow(D, y_axis='log')
        plt.colorbar(format='%+2.0f dB')
        plt.title('对数频率功率谱')

        plt.show()

class VideoPlotter(Plotter):
    def __init__(self, data):
        super().__init__(data)
        self._gif = None

    def plot(self):
        cap = cv2.VideoCapture(self._data)
        fps = cap.get(cv2.CAP_PROP_FPS)
        start_time = 1 * fps
        end_time = 5 * fps
        print(start_time, end_time)
        image_list = []
        i = 0

        for i in range(int(end_time)):
            ret, frame = cap.read()
            if ret == False:
                break
            frame = cv2.flip(frame, 0)
            frame = cv2.flip(frame, 1)
            if i >= start_time:
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                image_list.append(frame_rgb)

        cap.release()
        cv2.destroyAllWindows()

        self._gif = GifPlotter(image_list)
        self._gif.plot('list')

def main():
    #绘制数据点型数据
    pointlist = [Point(0, 0), Point(1, 2), Point(3, 1)]
    plotter_point = PointPlotter(pointlist)
    plotter_point.plot('line')
    
    #绘制多维数组型数据
    arr = np.array([[1, 2], [3, 4], [5, 6]])
    plotter_array = ArrayPlotter(arr)
    plotter_array.plot()

    #绘制文本型数据词云图
    chinese_text = ['程序设计好', '程序设计很好', '我喜欢程序设计', '程序设计作业']
    plotter_text = TextPlotter(chinese_text)
    plotter_text.plot(5)

    #读取图片路径并分行列显示
    image_path = 'E:\\图片\\克里斯保罗'
    plotter_image = ImagePlotter(image_path)
    plotter_image.plot(3, 3, (10, 8))

    #读取图片路径并输出为gif
    plotter_gif = GifPlotter(image_path)
    plotter_gif.plot()

    #对多维数组降维后绘制
    data = np.array([[1, -1, 2], [3, 10, -5], [-3, 4, 7]])
    plotter_keyfeature = KeyFeaturePlotter(data)
    plotter_keyfeature.plot()

    #对音频可视化
    music_file = 'E:\\CloudMusic\\Hall of Fame.mp3'
    plotter_music = MusicPlotter(music_file)
    plotter_music.plot()

    #对视频帧采样输出为gif
    video_file = 'E:\\图片\\VID_20210702_214821.mp4'
    plotter_video = VideoPlotter(video_file)
    plotter_video.plot()

if __name__ == '__main__': main()