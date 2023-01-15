import os
import cv2
import itertools
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageFilter

class Filter:                  #基类
    def __init__(self, im):
        self._image = im
        self._args = []
    
    def filter(self):  #滤波方法
        pass

class Null(Filter):
    def filter(self):
        return self._image

class EdgeExtraction(Filter):  #边缘提取
    def filter(self):
        return self._image.filter(ImageFilter.FIND_EDGES)

class Sharpen(Filter):         #锐化
    def filter(self):
        return self._image.filter(ImageFilter.SHARPEN)

class Blur(Filter):            #模糊
    def filter(self):
        return self._image.filter(ImageFilter.BLUR)

class Contour(Filter):         #轮廓滤波
    def filter(self):
        return self._image.resize(ImageFilter.CONTOUR)
    
class EdgeEnhance(Filter):     #边缘增强滤波
    def filter(self):
        return self._image.resize(ImageFilter.EDGE_ENHANCE)

class SizeAdjustment(Filter):  #大小调整
    def filter(self, shape):
        return self._image.resize(shape, Image.ANTIALIAS)

class ImageShop:
    '''
    Proceeed images, display and save.
    '''
    def __init__(self):
        self._image_list = []
        self._new_image_list = []
    
    def get_new_image_list(self):
        return self._new_image_list

    def __batch_ps(self, opt, ifnew, num, *args):
        '''
        opt: type of filter
        ifnew: set up a new image(1) or cover the initial image(0)
        num: number of the image
        *args: optional arguments of opt
        '''
        print(opt)
        if ifnew or num == 0:  #每张图片分别应用不同方法（新建）
            for im in self._image_list:
                image_instance = eval(opt)(im)
                self._new_image_list.append(image_instance.filter(*args))
        else:                  #将各种方法同时应用于一张图片（覆盖）
            for i in range(len(self._new_image_list)):
                image_instance = eval(opt)(self._new_image_list[i])
                self._new_image_list[i] = image_instance.filter(*args)                

    def load_images(self, form, file_dir):
        '''
        Load images in specific form from file_dir.
        '''
        if os.path.isdir(file_dir):  #目录
            file_names = os.listdir(file_dir)
            for file_name in file_names:
                if file_name[-len(form):] == form: 
                    image_file = file_dir + '\\' + file_name
                    self._image_list.append(Image.open(image_file))
        else:                        #文件
            self._image_list.append(Image.open(file_dir))

    def batch_ps(self, ifnew, *args):
        '''
        Proceed images.
        '''
        for i in range(len(args)):
            arg = args[i]
            if len(arg) > 1:
                self.__batch_ps(arg[0], ifnew, i, *arg[1:])
            else:
                self.__batch_ps(arg[0], ifnew, i)

    def display(self, num_row, num_column, fig_size, maxnum):
        '''
        Display images up to maxnum in the given figure.
        maxnum: The max number of images shown on the figure.
        '''
        plt.figure(figsize=fig_size)
        for i in range(min(maxnum, len(self._new_image_list))):
            plt.subplot(num_row, num_column, i + 1)
            plt.imshow(self._new_image_list[i])
            plt.xticks([])
            plt.yticks([])
        plt.show()

    def save(self, form, *file_dir):
        if len(file_dir):  #如果给出目标目录
            file_dir = str(file_dir[0])
            file_dir += '\\'
        else:              #没有目标目录则与源代码保存在同一目录下
            file_dir = ''
        for i in range(len(self._new_image_list)):
            self._new_image_list[i].save(file_dir + str(i + 1) + '.' + form)

class ImageSimilarity:  #计算图片相似度
    '''
    Calculate the similarity between images.
    '''
    def __init__(self, ims, shape):
        self._shape = shape
        self._hashstr = []
        self._image = [cv2.cvtColor(np.asarray(im), cv2.COLOR_RGB2BGR) for im in ims]  #转为opencv格式方便后续处理
        self._matrix = []
    
    def cmpHash(self, shape):  #比较哈希值
        '''
        Return an adjacency matrix of the similarity between images.
        '''
        self._matrix = []
        for i in range(len(self._hashstr) - 1):
            tmp = []
            for j in range(i + 1, len(self._hashstr)):
                tmp.append(sum(c1 == c2 for c1, c2 in itertools.zip_longest(self._hashstr[i], self._hashstr[j])) /
                            (shape[0] * shape[1]))
            self._matrix.append(tmp)
        return self._matrix

    def aHash(self):    #均值哈希
        self._hashstr = []
        for im in self._image:
            im = cv2.resize(im, self._shape)
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            avg = np.mean(np.asarray(gray))
            tmp = np.asarray(gray > avg).flatten()
            self._hashstr.append([1 if i else 0 for i in tmp])
        return self.cmpHash(self._shape)
    
    def dHash(self):    #差值哈希
        self._hashstr = []
        for im in self._image:
            im = cv2.resize(im, (self._shape[0] + 1, self._shape[1]))
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            tmp = []
            for i in range(self._shape[0]):
                for j in range(self._shape[1]):
                    tmp.append(1 if gray[i, j] > gray[i, j + 1] else 0)
            self._hashstr.append(tmp)
        return self.cmpHash(self._shape)

    def pHash(self):    #感知哈希
        self._hashstr = []
        for im in self._image:
            im = cv2.resize(im, (32, 32))
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            dct = cv2.dct(np.float32(gray))
            dct_roi = dct[:10, :10]
            avg = np.mean(dct_roi)
            tmp = np.asarray(dct_roi > avg).flatten()
            self._hashstr.append([1 if i else 0 for i in tmp])
        return self.cmpHash((10, 10))

    def classify_3hist(self):  #三直方图
        pass

    def classify_1hist(self):  #单通道直方图
        pass

class TestImageShop:    #测试类
    def main(self):
        file_name = 'E:\\图片\\天津'

        shop1 = ImageShop()
        shop1.load_images('jpg', file_name)
        shop1.batch_ps(0, ('Null', ))
        new_image_list = shop1.get_new_image_list()
        sim = ImageSimilarity(new_image_list, (10, 10))
        print('均值哈希相似度：', sim.aHash(), sep='\t')
        print('差值哈希相似度：', sim.dHash(), sep='\t')
        print('感知哈希相似度：', sim.pHash(), sep='\t')
        # shop1.display(2, 2, (15, 15), 4)

        shop2 = ImageShop()
        shop2.load_images('jpg', file_name)
        shop2.batch_ps(0, ('Blur', ))
        new_image_list = shop2.get_new_image_list()
        sim = ImageSimilarity(new_image_list, (10, 10))
        print('均值哈希相似度：', sim.aHash(), sep='\t')
        print('差值哈希相似度：', sim.dHash(), sep='\t')
        print('感知哈希相似度：', sim.pHash(), sep='\t')
        shop2.display(2, 2, (12, 10), 4)
        shop2.save('jpg')

if __name__ == '__main__':
    imgtest = TestImageShop()
    imgtest.main()