import requests
import re
import pymssql
import matplotlib.pyplot as plt  # 数学绘图库
from PIL import Image
import numpy as np  # 科学数值计算包，可用来存储和处理大型矩阵
import jieba  # 分词库
from wordcloud import WordCloud, ImageColorGenerator  # 词云库
from selenium import webdriver
import time

def get_info(url,headers):
    "获取历史列表中的所有歌曲并将其写入数据库中，同时返回所有歌曲的id，以便后面获取歌词"
    """
    @url:历史列表中的URl
    @headers:请求头，带cookie
    """
    data = {
        'encSecKey': '0bf1ec70cf125612399e37d7dfb504d14d2394b8c96263dd89e2c75abe6ad9e6db058c2ff49c04f7108f387b64d6b9858b0f587ffca00491d20cc0be6c5bb51ff720694788f1ae7959c116d1cc89c48891b6a690945203ec173ab2d063c4c84e07a6128d8e3459e60d66bafe2d9fd6eb551b2c342ec810dbde7e3e4aea3e062f',
        'params': 'CuBUXLB1SXVHZiy2D+ZEbN56uapUHOR8Ro4Q559tqnSGZy3PWL2neZhcPj/A2nuhDAZBwJVQamn9DBvMF9oe3+yMy5GogaoK4c3OLpTjZBZJRcTpY93E7WHEBdKdXO+mlwGFta2LOqHXMNK6bYKlr//G7097eAh2z75jtOMT6/9w3NFe4m0P7bvwl/05kHAIm/lsl+fondNUSUYikUybI06bOADb71bhgPp0MKX4K0w='
    }
    html = requests.post(url,data=data,headers=headers)
    html.encoding='utf-8'
    lmusic = html.json()['allData']
    listid = []
    try:
        connet = pymssql.connect(host='127.0.0.1',user='sa',password='123456',database='WebSpider')#参数的数据库
    except pymssql.OperationalError as p:#异常处理
        print(p)
    else:
        cursor = connet.cursor()
        for music in lmusic:
            playCount=music['playCount']
            mname=music['song']['name']
            mid=music['song']['id']
            listid.append(mid)
            musicer = music['song']['ar'][0]['name']
            print("正在向数据库插入%s的信息"%mname)
            if '\'' in mname:
                #对带有单引号的内容进行转义，不然插入数据库会报错
                mname=mname.replace('\'','\'\'')
                sql = "insert into Music_wyy_2019 values ('%d','%s','%s','%d')" % (mid, mname, musicer, playCount)
            else:
                sql = "insert into Music_wyy_2019 values ('%d','%s','%s','%d')" % (mid, mname, musicer, playCount)
            cursor.execute(sql)
        connet.commit()
    finally:
        connet.close()
        print("数据库已关闭")
    return listid

def get_lyric(mid,path):
    "获取所有歌曲的歌词"
    """
    @mid:歌曲id的列表
    @path:歌词保存的位置
    """
    try:
        file = open(path, 'w+',encoding='utf-8')
    except FileNotFoundError as FE:
        print(FE)
    else:
        #循环歌曲ID列表，获取歌词并写入指定的位置中
        for id in mid:
            print("开始获取%d的歌词"%id)
            url = 'http://music.163.com/api/song/media?id={id}'.format(id=id)
            browser = webdriver.Chrome()
            #打开页面，获取歌词
            browser.get(url)
            time.sleep(10)
            ele = browser.find_element_by_tag_name('body')
            content = ele.text
            # print("content=",content)
            #通过正则获取歌词
            r = r'.*"lyric":"(.*)\\n'
            p = re.compile(r)
            lyric = p.findall(content)
            # print("lyric=",str(lyric))
            #将获取的歌词写进指定的文件中
            file.write(str(lyric))
            browser.close()
    finally:
        file.close()
        print("歌词写入结束，文件已关闭")

def get_wordcloud(txt_path,backimage_path,font_path,save_path):
    "生成对应的词云图"
    """
    @txt_path:生成词云的TXT文件路径
    @backimage_path:词云的背景图片
    @save_path:生成的词云保存的位置
    """
    # 1、读入txt文本数据
    text = open(txt_path, "r",encoding='utf-8').read()
    # 2、结巴分词:cut_all参数可选, True为全模式，False为精确模式,默认精确模式
    cut_text = jieba.cut(text, cut_all=False)
    result = "/".join(cut_text)  # 必须给个符号分隔开分词结果,否则不能绘制词云
    # 3、初始化自定义背景图片
    image = Image.open(backimage_path)
    graph = np.array(image)
    # 4、产生词云图
    # 有自定义背景图：生成词云图由自定义背景图像素大小决定
    wc = WordCloud(font_path=font_path, background_color='white', max_font_size=100, mask=graph,random_state=30,max_words=500)
    wc.generate(result)
    # 5、绘制文字的颜色以背景图颜色为参考
    image_color = ImageColorGenerator(graph)  # 从背景图片生成颜色值
    # wc.recolor(color_func=image_color)  #使图片颜色跟字体颜色一样
    wc.to_file(save_path)  # 按照背景图大小保存绘制好的词云图，比下面程序显示更清晰
    # 6、显示图片
    plt.figure("词云图")  # 指定所绘图名称
    plt.imshow(wc)  # 以图片的形式显示词云
    plt.axis("off")  # 关闭图像坐标系
    plt.show()

if __name__ == '__main__':

    headers = {
        'Cookie': '_ntes_nuid=d7e9e203103e6e3159c61d3ad741c4f6; WM_TID=YmcEq9T7EEpAREBBUBc/T6sGRoFhDyYX; mail_psc_fingerprint=33b743fa72b3731f6ff0f9fcaa6d0dff; NMTID=00On98HU62a5TfueEpVlYyIe2CiHKsAAAF09r1GvA; __oc_uuid=b251ccd0-8b72-11eb-a20f-258991615aef; WEVNSM=1.0.0; WNMCID=kmpouj.1622641582421.01.0; _ntes_nnid=d7e9e203103e6e3159c61d3ad741c4f6,1630228381975; UM_distinctid=17c895761d710ef-0bea3e90a7a8c7-b7a1438-144000-17c895761d8e25; NTES_CMT_USER_INFO=33918545|winzsh2012|http://cms-bucket.nosdn.127.net/2018/08/13/078ea9f65d954410b62a52ac773875a1.jpeg|false|d2luenNoMjAxMkAxNjMuY29t; vinfo_n_f_l_n3=06db26c2779c121e.1.0.1639230744187.0.1639230751693; nts_mail_user=winzsh2012@163.com:-1:1; NTES_P_UTID=9ZEbpBXQzioBnonbQci2mBXfXhziw9EX|1648564820; P_INFO=winzsh2012@163.com|1648564820|0|mail163|00&99|bej&1648303983&mail163#bej&null#10#0#0|&0|mail163|winzsh2012@163.com; WM_NI=TvVRfYTmY4HAWEhR3B5NJSXKKsen2ETWR64eMXQ5Kkg0h/s+CTC/is4vC5eFyNJXy7yjZ31PvT8ZwgP0MogA6vO4our+I37/zYoEV798E1JoiCNkrlPKilvX5waKTzBzYzQ=; WM_NIKE=9ca17ae2e6ffcda170e2e6ee8be65bad93b8a2e23df6ef8eb3d54f868a8abaf525f5bf878fbc619293a9dac12af0fea7c3b92a98aa9ab3e55398b397d5cb4b959ba8b3b24af79286b4db4189adab8fb14f98899ed7b76f8f889fd6ca61a5f0a8d0f221818c8dd0ec79f8aa8dd6e84ebb9286b9fc3dbbb696d4b45cb68cf8bbf66d94f08390e64bf6aa81d5ee7fb2f587d4b625ba87a1a6d53dfbe88bd2c965ab9d828cf1689495a78df554f7a9afacd77282a6979bd437e2a3; _iuqxldmzr_=33; JSESSIONID-WYYY=vmjWYTXzUJm3XsZbAxvNlUln/kyToWTubyJkQu6TRtvt1Q4ua2ZqZW1GlzoSTISH/H37npJzH5g2KVvfe68aP8SS0d/IZOBW/941WAu2yMUhjvk45FsVlP\ku0qdkDSeVCodEDAISzkHN46j5Gs1MyBQ4o6PPucTSmAUANoJws063far:1648643907272; __csrf=7c41b845dd36eef1fe8a6fe296528147; MUSIC_U=2a03838c38aa9c1f8fe44219db2daaa491c8362f1c947a63bae3fb400bc6d458993166e004087dd3d78b6050a17a35e705925a4e6992f61dfe3f0151024f9e31; ntes_kaola_ad=1',
        'Host': 'music.163.com',
        'Referer': 'https://music.163.com/user/home?id=528083301',#参数->浏览器Network获取或抓包获取request中的cookie
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.82 Safari/537.36'
    }
    # 调用函数，并返回所有历史列表歌曲的Id
    url = 'https://music.163.com/weapi/v1/play/record?csrf_token=7c41b845dd36eef1fe8a6fe296528147'#参数->浏览器Network获取或抓包获取request中的cookie
    mid = get_info(url, headers)
    #调用函数，获取歌词，写入文件中
    # 自定义歌词下载的路径
    txt_path = r'E:\BaiduNetdiskDownload\Music.txt'
    get_lyric(mid,txt_path)
    # 词云的背景图，需要自己提前下载好
    backimage_path = r'E:\BaiduNetdiskDownload\wyy\9.jpg'
    # 指定生成词云保存的位置
    save_path = r"E:\BaiduNetdiskDownload\wyy\wordcloud.png"
    #词云生成需要用的字体路径，如果没有需要自己取下载
    font_path=r"E:\BaiduNetdiskDownload\wyy\simhei.ttf"
    get_wordcloud(txt_path,backimage_path,font_path,save_path)