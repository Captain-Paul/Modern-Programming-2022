import gevent
from gevent import monkey, pool

monkey.patch_all()  #将第三方库标记为IO非阻塞

import time
import requests
import pandas as pd
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

img_path = 'E:\\图片\\网易云民谣歌单\\'
csv_path = 'E:\\BUAA\\大三上\\程设\\week14\\songlist_info.csv'

p = pool.Pool(2000)
jobs = []
songlists = []
df = pd.DataFrame(columns=['id', 'title', 'user_id', 'user_name', 'description', 'num_songs',
                                'counts_play', 'counts_add', 'counts_share', 'num_comments'])

def produce_pages(url):
    print(f'Start get page {url}')
    response = requests.get(url=url, headers=headers)  #IO
    html = response.text
    soup = BeautifulSoup(html, 'html.parser')
    page = soup.select('.dec a')
    return page

def get_each_songlist(info):
    url = 'https://music.163.com' + info['href']   #歌单的url
    print(f'Start get songlist {url}')
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

    img_link = soup.find('img')['src']
    img = requests.get(img_link)  #IO
    image = Image.open(BytesIO(img.content))
    image.save(img_path + songlist_id + '.png')

    return [
        songlist_id, songlist_title, user_id, user_name, description, num_songs, 
        play_count, add_count, share_count, num_comments
    ]

if __name__ == '__main__':
    st = time.time()

    ## 首先爬取歌单所在页
    for i in range(0, 1500, 35):
        url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=' + str(i)
        jobs.append(p.spawn(produce_pages, url))
    gevent.joinall(jobs)

    ## 对每一页分别爬取歌单
    for job in jobs:
        page = job.value
        for info in page:
            songlists.append(p.spawn(get_each_songlist, info))
    gevent.joinall(songlists)

    for songlist in songlists:
        df.loc[len(df.index)] = songlist.value
    df.to_csv(csv_path, index=False)

    print('Total Time: {}s'.format(time.time() - st))