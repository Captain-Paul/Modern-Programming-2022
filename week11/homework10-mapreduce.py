import time
import json
import jieba
import pandas as pd
from tqdm import tqdm
from matplotlib import pyplot as plt
from multiprocessing import Pool, Manager, Process

def read_data(file_name):
    news_list = []
    with open(file_name, encoding='utf-8') as f:
        data = json.load(f)
        news_list = [news.get('content') for news in data]
    return news_list

def make_stop_words(file_name):
    stop_words = set()
    stop_f = open(file_name, 'r', encoding='utf-8')
    jieba.load_userdict(file_name)
    for line in stop_f:
        line = line.rstrip('\n')
        if len(line):
            stop_words.add(line)
    stop_f.close()
    return stop_words

def my_map1(raw_list, stop_words):
    counts = {}
    for content in tqdm(raw_list):
        # content = raw_list.pop(0)
        seg_list = jieba.lcut(content)
        for word in seg_list:
            if word not in stop_words:
                counts[word] = counts.get(word, 0) + 1
    return counts

def my_reduce1(final_dict, result_list, file_path):
    for item in result_list:
        final_dict = dict(final_dict, **item)
    final_dict = dict(sorted(final_dict.items(), key=lambda dc:dc[1], reverse=True))
    df_dict = pd.DataFrame(list(final_dict.items()), columns=['words', 'count'])
    df_dict.to_csv(file_path, index=False)

if __name__ == '__main__':
    manager = Manager()
    news_list = manager.list(read_data('sohu_data.json')[:20000])
    stop_words = make_stop_words('stopwords_list.txt')
    result_dict = manager.dict()
    result = []
    num_news = len(news_list)

    num_process_list = [1, 2, 4, 6, 8, 10]
    total_time_list = []
    for num_processes in num_process_list:
        pool = Pool(processes=num_processes)
        start_time = time.time()
        for i in range(num_processes):
            result.append(pool.apply_async(my_map1, (news_list[i * (num_news // num_processes) : (i + 1) * (num_news // num_processes)], stop_words)))
        pool.close()
        pool.join()
    
        dic_list = manager.list([item.get() for item in result])  # 转为Manager.list, 以实现进程间通信
        process_reduce = Process(target=my_reduce1, args=(result_dict, dic_list, 'counts_' + str(num_processes) +'.csv'))
        process_reduce.start()
        process_reduce.join()

        end_time = time.time()
        total_time_list.append(end_time - start_time)
    
    print(total_time_list)
    plt.figure()
    plt.plot(num_process_list, total_time_list)
    plt.show()