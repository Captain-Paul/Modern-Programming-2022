import os
import re
import sys
import time
import pygame
import pysnooper
import pandas as pd
from tqdm import tqdm
from functools import wraps
from memory_profiler import profile
from line_profiler import LineProfiler

def check_path(file_path):
    '''
    Check the existence of file_path.
    If not, create it.
    '''
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if os.path.exists(file_path):
                print('Path successfully accessed')
            else:
                print('The path does not exist!')
                os.makedirs(file_path)
            return func(*args, **kwargs)
        return wrapper
    return decorator

class Music:
    '''
    Play specific music according to the type of returned values.
    '''
    def __init__(self, music_path):
        self._path = music_path
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            pattern = re.compile(r'\'(.*?)\'')
            pygame.init()
            pygame.mixer.init()
            result = func(*args, **kwargs)
            if type(result) == tuple:  #多个返回值
                for res in result:
                    type_name = pattern.findall(str(type(res)))
                    pygame.mixer.music.load(self._path + '\\' + type_name[0] + '.mp3')
                    pygame.mixer.music.play()
                    time.sleep(3)
                    pygame.mixer.music.stop()
            else:                      #单个返回值
                type_name = pattern.findall(str(type(result)))
                pygame.mixer.music.load(self._path + '\\' + type_name[0] + '.mp3')
                pygame.mixer.music.play()
                time.sleep(3)
                pygame.mixer.music.stop()
            return result
        return wrapper

class TempSave:
    '''
    Save the printed content of the function to file_dir.
    '''
    def __init__(self, file_dir):
        self._file = file_dir
    
    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            old_out = sys.stdout
            sys.stdout = open(self._file, 'w', encoding='utf-8')
            func(*args, *kwargs)
            sys.stdout.close()
            sys.stdout = old_out
        return wrapper

class BigDataStructure:
    def __init__(self):
        self._df = pd.DataFrame()
        self._list = []
    
    @profile    #查看内存使用情况
    @pysnooper.snoop(output='load_debug.log')
    def load(self, file_path):
        self._df = pd.read_csv(file_path, sep='\t', encoding='utf-8').drop_duplicates()
        self._list = list(self._df['text'])

    @pysnooper.snoop(output='traverse_debug.log')
    def traverse(self):  #时间消耗大的函数
        i = 0
        for index, row in tqdm(self._df.iterrows(), desc='DataFrame'): #进度条
            i += 1
        for index in tqdm(range(len(self._list)), desc='list'):
            i += 1
        print(i)

path = 'E:\\CloudMusic'
@check_path(path)
@Music(path)       #音乐文件路径
def add(a, b):
    return str(a), b

@TempSave('E:\\BUAA\\大三上\\程设\\week8\\tempout.txt')  #输出内容保存路径
def print_num(n):
    for i in range(n):
        print(i + 1)

def main():
    print(add(1, 2))
    print_num(10)

    data = BigDataStructure()
    data.load('E:\\BUAA\\大三上\\程设\\week3\\weibo.txt')

    lp = LineProfiler(data.traverse)  #逐行代码时间分析
    lp.enable()
    data.traverse()
    lp.disable()
    lp.print_stats()

if __name__ == '__main__': main()