import re
import jieba
import numpy as np
import pandas as pd
import seaborn as sns
from tqdm import tqdm
import matplotlib.pyplot as plt

class Tokenizer:
    '''
    Tokenize Chinese texts based on words or characters.
    '''
    def __init__(self, chars, coding='c', PAD=0):
        '''
        chars: list of strings(texts)
        coding: 'c': split based on characters
                'w': split based on words
        PAD: id of null

        Build a dictionary to differentiate words and characters.
        '''
        self.dic = {'[PAD]':PAD}
        self.tot = 0
        self.chars = chars
        self.coding = coding
        self.PAD = PAD
        if coding == 'c':  #按字
            for content in tqdm(chars):
                for character in content:
                    if character not in self.dic:
                        self.tot += 1
                        self.dic[character] = self.tot
        else:
            for content in tqdm(chars):
                seg_list = jieba.lcut(content)
                for word in seg_list:
                    if word not in self.dic:
                        self.tot += 1
                        self.dic[word] = self.tot

    def tokenize(self, sentence):
        '''
        Return a list of words or characters based on the given sentence.
        '''
        if self.coding == 'w':
            return jieba.lcut(sentence)
        return list(sentence)

    def encode(self, list_of_chars):
        '''
        Return a list of numbers based on the dictionary.
        '''
        return [self.dic[item] for item in list_of_chars]

    def trim(self, tokens, seq_len):
        '''
        Adjust the length of tokens to seq_len.
        '''
        length = len(tokens)
        if length < seq_len:
            tokens.extend([self.PAD] * (seq_len - length))
        elif length > seq_len:
            tokens = tokens[:seq_len]
        return tokens

    def decode(self, tokens):
        '''
        Translate numbers to sentences(list).
        '''
        # return [filter(lambda k: self.dic[k] == token, self.dic) for token in tokens]
        list_of_values = list(self.dic.values())
        list_of_keys = list(self.dic.keys())
        return [list_of_keys[list_of_values.index(token)] for token in tokens]
        
    def encode_all(self, seq_len):
        '''
        Return tokens of all texts(chars) with length of seq_len.
        '''
        tokens = []
        if self.coding == 'c':
            for content in tqdm(self.chars):
                list = self.trim(self.encode(content), seq_len)
                tokens.append(list)
        else:
            for content in tqdm(self.chars):
                list = jieba.lcut(content)
                list = self.trim(self.encode(list), seq_len)
                tokens.append(list)
        return tokens

def clean_segment(text_list):
    '''
    clean text(url, @ etc.) and segment words.
    '''
    seg_list = []
    for text in tqdm(text_list):
        if type(text) != str:
            continue
        text = re.sub(r'(回复)?(//)?\s*@\S*?\s*(:| |$)', ' ', text)     # 去除正文中的@和回复/转发中的用户名
        # text = re.sub(r'\[\S+\]', '', text)     # 去除表情符号
        text = re.sub('http\S+', '', text)       # 去除网址
        text = text.replace("转发微博", '')       # 去除无意义的词语
        text = text.replace('我在:', '')
        text = text.replace('我在这里:', '')
        text = re.sub(r'\s+', ' ', text)    # 合并正文中过多的空格
        seg_list.append(text)
    return seg_list

if __name__ == '__main__':
    df = pd.read_csv('final_none_duplicate.txt', sep='\t', encoding='utf-8')
    df.columns = ['location', 'text', 'user_id', 'time']
    texts = list(df['text'])
    texts = clean_segment(texts)

    len_dist = np.array([len(text) for text in texts])
    seq_len_c = int(np.mean(len_dist))  #以平均字数作为seq_len
    sns.displot(len_dist)
    plt.show()

    tokenizer_c = Tokenizer(texts)
    tokens_c = tokenizer_c.encode_all(seq_len_c)
    print(tokens_c[:5])
    print(tokenizer_c.decode(tokens_c[0]))
    
    print()

    tokenizer_w = Tokenizer(texts, coding='w')
    # seq_len_w = int(np.mean(np.array([len(jieba.lcut(text)) for text in texts])))  #以平均词数作为seq_len
    tokens_w = tokenizer_w.encode_all(seq_len_c//2)  #以平均字数的一半作为seq_len
    print(tokens_w[:5])
    print(tokenizer_w.decode(tokens_w[0]))