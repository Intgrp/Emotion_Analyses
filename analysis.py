#coding=utf-8

import nltk
import xlrd
import pickle
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist
import sklearn
import pandas as pd
import numpy as np
import jieba
#import snownlp
import jieba.posseg as pseg
from gensim import corpora, models, similarities
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.sklearn

#把所有词作为特征
def bag_of_words(words):
    return dict([(word, True) for word in words])

#把双词搭配（bigrams）作为特征
def bigram(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)  #把文本变成双词搭配的形式
    bigrams = bigram_finder.nbest(score_fn, n) #使用了卡方统计的方法，选择排名前1000的双词
    return bag_of_words(bigrams)

#把所有词和双词搭配一起作为特征
def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=1000):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)  #所有词和（信息量大的）双词搭配一起作为特征

def pre_process(filename='data/train.xlsx'):
    df = pd.read_excel(filename)
    #去掉主题是空行的，就是啥都没有的那些数据
    NONE_VIN = (df["theme-主题"].isnull()) | (df["theme-主题"].apply(lambda x: str(x).strip("NULL;").isspace()))
    df_null = df[NONE_VIN]
    df_not_null = df[~NONE_VIN]
    #去掉主题和情感关键词都是NULL的数据，因为这些是没用的
    #dd = df_not_null[~(df_not_null['theme-主题'].apply(lambda x: str(x).strip("NULL;").strip()==''))]
    return df_not_null
def chinese_word_cut(mytext):
    return " ".join(jieba.cut(mytext))

def word_cut(df):
    nwordall = []
    for t in df['content-评论内容']:
        words = pseg.cut(t)
        nword = ['']
        for w in words:
            if ((w.flag == 'n' or w.flag == 'v' or w.flag == 'a') and len(w.word) > 1):
                nword.append(w.word)
        nwordall.append(nword)
    print(nwordall)
def deal(df):
    #从文本中提取1000个最重要的特征关键词，然后停止
    n_features = 1000
    #关键词提取和向量转换过程
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words='english',
                                    max_df=0.5,
                                    min_df=10)
    tf = tf_vectorizer.fit_transform(df["content_cutted"])

    #应用LDA方法，指定（或者叫瞎猜）主题个数
    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    lda.fit(tf)
    n_top_words = 20
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
    #pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)

def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


df = pre_process()
df["content_cutted"] = df['content-评论内容'].apply(chinese_word_cut)
deal(df)

