import time
import asyncio
import aiohttp
import pandas as pd
from bs4 import BeautifulSoup

headers = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
}

img_path = 'E:\\图片\\网易云民谣歌单\\'
csv_path = 'E:\\BUAA\\大三上\\程设\\week14\\songlist_info.csv'

df = pd.DataFrame(columns=['id', 'title', 'user_id', 'user_name', 'description', 'num_songs',
                                'counts_play', 'counts_add', 'counts_share', 'num_comments'])

async def get_pages(url_page):
    print(f'Start visit url {url_page}')

    async with aiohttp.ClientSession() as session_page:
        async with session_page.get(url_page, headers=headers) as response_page:
            html_page = await response_page.text()
            soup = BeautifulSoup(html_page, 'html.parser')
            page = soup.select('.dec a')
            for info in page:
                url = 'https://music.163.com' + info['href']
                async with aiohttp.ClientSession() as session_list:
                    async with session_list.get(url, headers=headers) as response_list:
                        html_list = await response_list.text()
                        soup_list = BeautifulSoup(html_list, 'html.parser')
                        
                        songlist_id = info['href'].split('=')[-1]
                        songlist_title = info['title']
                        play_count = soup_list.find('strong', class_='s-fc6').text
                        share_count = soup_list.find('a', class_='u-btni u-btni-share')['data-count']
                        add_count = soup_list.find('a', class_='u-btni u-btni-fav').text.strip('\n')
                        user = soup_list.find('a', class_='s-fc7')
                        user_id = user['href'].split('=')[-1]
                        user_name = user.text

                        try:
                            description = soup_list.find('p', class_='intr f-brk').text.replace('\n', '').replace('\r', '')
                        except:
                            description = ''    #异常处理部分歌单描述标签不一致的情况

                        num_songs = soup_list.find('span', id='playlist-track-count').text
                        num_comments = soup_list.find('span', id='cnt_comment_count').text

                        df.loc[len(df.index)] = [
                            songlist_id, songlist_title, user_id, user_name, description, 
                            num_songs, play_count, add_count, share_count, num_comments
                        ]


if __name__ == '__main__':
    st = time.time()

    loop = asyncio.get_event_loop()
    tasks = []
    for i in range(0, 1500, 35):
        url = 'https://music.163.com/discover/playlist/?order=hot&cat=%E6%B0%91%E8%B0%A3&limit=35&offset=' + str(i)
        tasks.append(loop.create_task(get_pages(url)))
    loop.run_until_complete(asyncio.wait(tasks))

    df.to_csv(csv_path, index=False)

    print(f'Time: {time.time() - st}s')