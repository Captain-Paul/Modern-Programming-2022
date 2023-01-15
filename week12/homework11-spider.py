import time
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from queue import Queue
from bs4 import BeautifulSoup
from threading import Thread, Lock

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

img_path = 'E:\\图片\\网易云民谣歌单\\'
csv_path = 'E:\\BUAA\\大三上\\程设\\week12\\songlist_info.csv'

df = pd.DataFrame(columns=['id', 'title', 'user_id', 'user_name', 'description', 'num_songs',
                                'counts_play', 'counts_add', 'counts_share', 'num_comments'])
q = Queue()

class Producer(Thread):
    def __init__(self, url, lock):
        super().__init__()
        self._url = url
        self._lock = lock

    def run(self):
        with self._lock:
            response = requests.get(url=self._url, headers=headers)  #IO
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')
            page = soup.select('.dec a')
            q.put(page)

class Consumer(Thread):
    def __init__(self):
        super().__init__()

    def run(self):
        page = q.get()
        
        for info in page:
            url = 'https://music.163.com' + info['href']   #歌单的url
            response = requests.get(url=url, headers=headers)  #IO
            html = response.text
            soup = BeautifulSoup(html, 'html.parser')

            songlist_id = info['href'].split('=')[-1]
            songlist_title = info['title']
            play_count = soup.find('strong', class_='s-fc6').text
            share_count = soup.find('a', class_='u-btni u-btni-share')['data-count']
            add_count = soup.find('a', class_='u-btni u-btni-fav').text.strip('\n')
            user = soup.find('a', class_='s-fc7')
            user_id = user['href'].split('=')[-1]
            user_name = user.text

            try:
                description = soup.find('p', class_='intr f-brk').text.replace('\n', '').replace('\r', '')
            except:
                description = ''    #异常处理部分歌单描述标签不一致的情况

            num_songs = soup.find('span', id='playlist-track-count').text
            num_comments = soup.find('span', id='cnt_comment_count').text

            df.loc[len(df.index)] = [songlist_id, songlist_title, user_id, user_name, description, num_songs, play_count, add_count, share_count, num_comments]
            
            img_link = soup.find('img')['src']
            img = requests.get(img_link)  #IO
            image = Image.open(BytesIO(img.content))
            image.save(img_path + songlist_id + '.png')

if __name__ == '__main__':
    producer_list = []
    consumer_list = []
    lock = Lock()
    num_thread = 43

    st = time.time()
    for i in range(0, 1500, 35):
        url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=' + str(i)
        producer = Producer(url, lock)
        producer_list.append(producer)

    for i in range(num_thread):
        consumer = Consumer(q)
        consumer_list.append(consumer)

    for producer in producer_list:
        producer.start()
    for producer in producer_list:
        producer.join()

    for consumer in consumer_list:
        consumer.start()
    for consumer in consumer_list:
        consumer.join()

    df.to_csv(csv_path, index=False)

    print(time.time() - st)