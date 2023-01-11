import pandas as pd
import numpy as np
import random as rd
import jieba
import wordcloud
import warnings
from scipy.spatial import distance
from tqdm import tqdm
from sklearn.feature_extraction.text import TfidfVectorizer
from gensim.models import word2vec

warnings.filterwarnings('ignore')

def read_data(file_name):
    '''
    Read datafile in csv format.
    '''
    df = pd.read_csv(file_name, encoding='utf-8', usecols=[0])
    return list(df['content'])

def make_stop_words(file_name):
    '''
    Input stop-word list into jieba module.
    '''
    stop_f = open(file_name, 'r', encoding='utf-8')
    jieba.load_userdict(file_name)
    wordset = set()
    for line in stop_f:
        line = line.rstrip('\n')
        if len(line):
            wordset.add(line)
    stop_f.close()
    return wordset

def word_frequency(comments, stop_words):
    '''
    Segment words with jieba and count word frequency.
    '''
    counts = {}   # 词频统计
    seg_list = []   # 分词后的弹幕列表(弹幕储存为列表)
    documents = []   # 在词语之间添加空格的弹幕列表(弹幕储存为列表)
    if_stop_word = [0] * len(comments)  #第i条弹幕是否含有停用词
    i = 0
    for i in range(len(comments)):
        cur_seg_list = jieba.lcut(comments[i])
        seg_list.append(cur_seg_list)
        documents.append(' '.join(cur_seg_list))
        for seg in cur_seg_list:
            if seg not in stop_words:
                counts[seg] = counts.get(seg, 0) + 1
            else:
                if_stop_word[i] = 1
    counts = dict(sorted(counts.items(), key=lambda dc: dc[1], reverse=True))
    return seg_list, counts, documents, if_stop_word

def word_cloud(counts, n):
    '''
    Draw wordcloud image of top-n words.
    '''
    wordpng = wordcloud.WordCloud(background_color='white', height=700, width=1000, font_path='C:\Windows\Fonts\simHei.ttf')
    wordpng.generate(" ".join(list(counts.keys())[:n]))
    wordpng.to_file("Top_Wordcloud.png")

def screen_character_word(counts):
    '''
    Extract frequently used words as characteristic words.
    '''
    word_list = [key for key, value in counts.items() if value > 10]  #出现次数大于10的词语
    word_list = list(set(word_list))  #去重
    word_id = {}
    for i in range(len(word_list)):
        word_id[word_list[i]] = i
    return word_list, word_id

def Euclid_distance(v1, v2):
    return distance.euclidean(np.array(v1), np.array(v2))

def cosine_distance(v1, v2):
    return distance.cosine(np.array(v1), np.array(v2))
    
def inner_product(v1, v2):
    return np.dot(np.array(v1), np.array(v2))

def generate_random_comment():
    '''
    Generate a comment with at least one characteristic word 

    and the corresponding 0-1 vector randomly from the list.
    '''
    id = rd.randint(0, len(seg_list) - 1)
    while if_stop_word[id]:  #找到不是停用词的
        id = rd.randint(0, len(seg_list) - 1)
    random_vector = [0] * (len(character_word) + 5)
    for word in seg_list[id]:
        if word in character_word:
            random_vector[word_id[word]] = 1
    return comments[id], random_vector

def search_nearest_comment(random_vector):
    '''
    Search the comment nearest to the random one either in Euclid or cosine distance.
    '''
    mind_euclid = mind_cosine = 10000
    comment_euclid = comment_cosine = ''
    for content in tqdm(seg_list):
        content_vector = [0] * (len(character_word) + 5)
        for word in content:
            if word in character_word:
                content_vector[word_id[word]] = 1
        if sum(content_vector) == 0 or content_vector == random_vector:
            continue
        d1 = Euclid_distance(content_vector, random_vector)
        if mind_euclid > d1:
            mind_euclid = d1
            comment_euclid = content
        d2 = cosine_distance(content_vector, random_vector)
        if mind_cosine > d2:
            mind_cosine = d2
            comment_cosine = content
    return ''.join(comment_euclid), ''.join(comment_cosine)

def TF_IDF():
    '''
    用于特征词提取
    TF: frequency of occurrence  = (number of words) / N
    IDF: frequency of inverse document  = log(total number of documents / number of documents with word)
    '''
    vectorizer = TfidfVectorizer(max_df=0.5, stop_words=list(stop_words))
    vectorizer.fit_transform(documents)
    return vectorizer.get_feature_names_out()

def word_to_vec():
    sentences = word2vec.LineSentence('documents.txt')
    model = word2vec.Word2Vec(sentences, size=100, window=5, sg=0)
    return model

if __name__ == '__main__':
    comments = read_data('danmuku.csv')
    stop_words = make_stop_words('stopwords_list.txt')
    seg_list, counts, documents, if_stop_word = word_frequency(comments, stop_words)

    output_path = 'documents.txt'
    with open(output_path, 'w', encoding='utf-8') as wordfile:
        for sentence in documents:
            print(sentence, file=wordfile)

    print('TOP10词语: {}\n'.format(list(counts.keys())[:10]))
    dic_word = {'词语':counts.keys(), '次数':counts.values()}
    pd.DataFrame(dic_word).to_csv('word_counts.csv')
    word_cloud(counts, 50)

    character_word, word_id = screen_character_word(counts)
    print('词频特征词提取:', len(character_word), end='')
    for i in range(50):
        print(rd.choice(list(character_word)), end=',')
    print()

    random_list = []
    for i in range(5):
        content, vector = generate_random_comment()
        random_list.append(vector)
        print('随机生成弹幕', i + 1, ': ', content, sep='')
    euclid_dis = [[Euclid_distance(c1, c2) for c2 in random_list] for c1 in random_list]
    cos_dis = [[cosine_distance(c1, c2) for c2 in random_list] for c1 in random_list]
    print('随机弹幕对的欧几里得距离:\n', euclid_dis)
    print('随机弹幕对的余弦距离:\n', cos_dis)

    names = TF_IDF()
    print('TF-IDF特征词提取:', len(names), names[-50:])

    #抽取随机弹幕并寻找与之语义最接近的弹幕
    random_comment, random_vector = generate_random_comment()
    print('随机抽取弹幕为：{}\n'.format(random_comment))
    comment_euclid, comment_cosine = search_nearest_comment(random_vector)
    print('欧氏距离最接近弹幕为: {}\n余弦距离最接近弹幕为: {}\n'.format(comment_euclid, comment_cosine))