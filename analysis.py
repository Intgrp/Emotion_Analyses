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
from gensim.models import word2vec
import jieba.analyse

#预处理，去掉df里面的空行
def pre_process(filename='data/train.xlsx'):
    df = pd.read_excel(filename)
    #去掉主题是空行的，就是啥都没有的那些数据
    NONE_VIN = (df["theme-主题"].isnull()) | (df["theme-主题"].apply(lambda x: str(x).strip("NULL;").isspace()))
    df_not_null = df[~NONE_VIN]
    #增加content_cutted那一列，这一列先对数据去掉停用词，再分词
    df_not_null["content_cutted"] = df_not_null['content-评论内容'].apply(seg_stopword_sentence)

    return df_not_null



def chinese_word_cut(mytext):
    # 去掉停用词
    #jieba.analyse.set_stop_words(stpwrdlst)
    #a = jieba.analyse.extract_tags(mytext, topK=20, withWeight=False, allowPOS=())
    #分词
    #print(jieba.cut(mytext))
    return " ".join(jieba.cut(mytext))

# 创建停用词list
def stopwordslist(filepath):
    stopwords = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return stopwords

#对文本做停用词处理
def seg_stopword_sentence(sentence):
    sentence = sentence
    sentence_seged = jieba.cut(sentence)
    stopwords = stopwordslist('data/stopwords.txt')  # 这里加载停用词的路径
    outstr = ''
    for word in sentence_seged:
        if word not in stopwords:
            if word != '\t':
                outstr += word
                outstr += " "
    return outstr

#主要处理算法，TF-IDF、LDA
def deal(df,ss="content_cutted"):
    stopwords = stopwordslist('data/stopwords.txt')
    #从文本中提取1000个最重要的特征关键词，然后停止
    n_features = 1000
    #关键词提取和向量转换过程
    tf_vectorizer = CountVectorizer(strip_accents='unicode',
                                    max_features=n_features,
                                    stop_words=stopwords,
                                    max_df=0.5,
                                    min_df=10)
    tf = tf_vectorizer.fit_transform(df[ss])

    #应用LDA方法，指定（或者叫瞎猜）主题个数
    n_topics = 10
    lda = LatentDirichletAllocation(n_components=n_topics, max_iter=50,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)
    print("lda:",lda)
    lda.fit(tf)
    n_top_words = 20
    tf_feature_names = tf_vectorizer.get_feature_names()
    print_top_words(lda, tf_feature_names, n_top_words)
    #pyLDAvis.sklearn.prepare(lda, tf, tf_vectorizer)
    #model = word2vec.Word2Vec(df["content_cutted"], min_count=5, size=50)
    #model.save('word2vec_model')


def print_top_words(model, feature_names, n_top_words):
    for topic_idx, topic in enumerate(model.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
    print()


#df = pre_process()
#deal(df)
#new_model=word2vec.Word2Vec.load('word2vec_model')
