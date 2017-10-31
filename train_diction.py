#coding=utf-8
'''
根据链接http://blog.csdn.net/u012052268/article/details/77825981介绍，
把原始的训练数据里面的主题拿出来，作为一个一个的词制作成自定义字典，这样
再次对content识别的时候，就会把出现的词作为一个整体主题拿去判断，减少了
产生主题不一致的情况

把原始数据的情感关键词也拿出来，做自定义词典
'''

import jieba
import pandas as pd

dic_theme={}
dic_sentiment={}
def seg_sentence(sentence):
    words = str(sentence).replace("NULL;","").split(';')
    for w in words:
        if w not in dic_theme.keys() and "NULL"!=w and ""!=w:
            dic_theme[w]=1

def split_sentence(sentence):
    words = str(sentence).split(";")
    for w in words:
        if w not in dic_sentiment.keys() and ""!=w:
            dic_sentiment[w]=1

def theme_tiqu(filename='data/train.xlsx'):
    df = pd.read_excel(filename)
    # 去掉主题是空行的，就是啥都没有的那些数据
    NONE_VIN = (df["theme-主题"].isnull()) | (df["theme-主题"].apply(lambda x: str(x).strip("NULL;").isspace()))
    df_not_null = df[~NONE_VIN]
    df_not_null['theme-主题'].apply(seg_sentence)
    write_dic('data/theme_words.txt',dic_theme)

def sentiment_word_tiqu(filename='data/train.xlsx'):
    df = pd.read_excel(filename)
    df["sentiment_word-情感关键词"].apply(split_sentence)
    write_dic('data/sentiment_words.txt',dic_sentiment)

def write_dic(file_path,dic):
    file_object = open(file_path, 'w',encoding='UTF-8')
    for w in dic:
        if dic[w]==1:
            file_object.write(w+"\n")
        else:
            continue
    file_object.close()
    print("write finish!!!")

def split_sentiment(filename='data/train.xlsx'):
    df = pd.read_excel(filename)
    #df.loc[:, [u'sentiment_word-情感关键词', u'sentiment_anls-情感正负面']].apply(test)
    for i in range(len(df)):
        ss = str(df.loc[i,'sentiment_word-情感关键词']).split(";")
        tt = str(df.loc[i,'sentiment_anls-情感正负面']).split(";")
        for i in range(len(ss)):
            if ss[i] not in dic_sentiment.keys() and ""!=ss[i]:
                dic_sentiment[ss[i]]=tt[i]
    write_sentiment('data/sentiment_words_正负面.txt',dic_sentiment)

def write_sentiment(file_path,dic):
    file_object = open(file_path, 'w', encoding='UTF-8')
    for w in dic:
        file_object.write(w + " "+dic[w]+"\n")
    file_object.close()
    print("write finish!!!")
# jieba.load_userdict('userdict.txt')
#theme_tiqu()
#sentiment_word_tiqu()

#df = pd.read_excel('data/train.xlsx')
#提取这两列数据
#df['sentiment_anls-情感正负面'].apply(test)
#df.loc[:,[u'sentiment_word-情感关键词',u'sentiment_anls-情感正负面']].apply(test)
split_sentiment()