import time
import asyncio
import aiohttp
import psycopg2
from datetime import datetime
from bs4 import BeautifulSoup

conn = psycopg2.connect(
    database='CloudMusic',
    user='postgres',
    password='123456',
    host='127.0.0.1',
    port='5432'
)
conn.set_client_encoding('utf-8')
cur = conn.cursor()

sql_drop = 'DROP TABLE Songlist;'
cur.execute(sql_drop)
conn.commit()

sql_create = '''CREATE TABLE Songlist (
                    id VARCHAR PRIMARY KEY,
                    title VARCHAR,
                    text VARCHAR,
                    author VARCHAR,
                    date DATE,
                    related_articles VARCHAR,
                    mp3_path VARCHAR
                );'''
cur.execute(sql_create)
conn.commit()

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

def set_encoding(items):
    lis = []
    for item in items:
        if type(item) == str:
            lis.append(item.encode('utf-8'))
        else:
            lis.append(item)
    return tuple(lis)

async def get_pages(url_page):
    print(f'Start visit url {url_page}')

    async with aiohttp.ClientSession() as session_page:
        async with session_page.get(url_page, headers=headers) as response_page:
            html_page = await response_page.text()
            soup = BeautifulSoup(html_page, 'html.parser')
            page = soup.select('.dec a')
            for info in page:
                url = 'https://music.163.com' + info['href']
                print(f'Start visit url {url}')
                async with aiohttp.ClientSession() as session_list:
                    async with session_list.get(url, headers=headers) as response_list:
                        html_list = await response_list.text()
                        soup_list = BeautifulSoup(html_list, 'html.parser')
                        
                        songlist_id = info['href'].split('=')[-1]
                        songlist_title = info['title']
                        user = soup_list.find('a', class_='s-fc7')
                        user_name = user.text
                        date_str = soup_list.find('span', class_='time s-fc4').text[:10]
                        date = datetime.strptime(date_str, '%Y-%m-%d')
                        related = ''
                        path = 'E:\\CloudMusic\\'

                        try:
                            description = soup_list.find('p', class_='intr f-brk').text.replace('\n', '').replace('\r', '')
                        except:
                            description = ''    #异常处理部分歌单描述标签不一致的情况

                        sql_insert = '''INSERT INTO 
                                            Songlist(id, title, text, author, date, related_articles, mp3_path)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s);
                                        '''
                        items = (songlist_id, songlist_title, description, user_name, date, related, path)
                        items = set_encoding(items)
                        cur.execute(sql_insert, items)
                        conn.commit()

if __name__ == '__main__':
    st = time.time()

    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(0, 1500, 35):
        url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=' + str(i)
        tasks.append(loop.create_task(get_pages(url)))
    loop.run_until_complete(asyncio.wait(tasks))

    cur.close()
    conn.close()
    print(f'Time: {time.time() - st}s')