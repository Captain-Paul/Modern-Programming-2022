import os
import random
import numpy as np
from PIL import Image

def random_walk(miu, x0, sigma, N):
    x = x0
    yield x
    for i in range(N - 1):
        w = random.normalvariate(0, sigma)
        x += miu + w
        yield x

class FaceDataset:
    def __init__(self, path_list):
        self._path_list = path_list
        self._now = 0
        self._image_list = []

    def load_image(self, img_path):
        img = Image.open(img_path)
        return np.array(img)

    def __iter__(self):
        return self

    def __next__(self):
        self._image_list = []
        if self._now < len(self._path_list):
            path = self._path_list[self._now]
            img_list = os.listdir(path)
            for img_name in img_list:
                img = path + '\\' + img_name
                self._image_list.append(self.load_image(img))
            self._now += 1
            return self._image_list
        else:   #遍历结束
            raise StopIteration()            

def get_image_dir(path):
    list_dir = os.listdir(path)
    if os.path.isdir(path + '\\' + list_dir[0]):  #未到目标文件夹
        for folder_name in list_dir:
            yield from get_image_dir(path + '\\' + folder_name)  #递归子文件夹
    else:   #到目标文件夹
        yield path  

def main():
    for val1, val2 in zip(random_walk(1, 1, 1, 10), random_walk(0, 0.5, 2, 10)):
        print(val1, val2)

    base_path = "E:\\BUAA\\大三上\\程设\\week9\\originalPics"
    path_list = list(get_image_dir(base_path))  #获取所有图片目录
    dataset = FaceDataset(path_list)
    for image_list in dataset:
        print(image_list[0].shape)

if __name__ == '__main__': main()