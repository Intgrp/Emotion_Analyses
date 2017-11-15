import pandas as pd
import analysis
import jieba
from jieba import analyse

#加载主题词典
def load_theme_words(filepath='data/theme_words.txt'):
    theme_words = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return theme_words

#加载情感词典
def load_sentiment_words(filepath='data/sentiment_words_正负面.txt'):
    theme_words={}
    for line in open(filepath, 'r', encoding='utf-8').readlines():
        tt = line.split()
        #print("tt[0]:",tt[0],"tt[1]:",tt[1])
        theme_words[tt[0]]=tt[1]
    #temp = [line.strip().split() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    print("theme_words:",theme_words)
    return theme_words

#theme是已经分好词的每行词间用空格隔开的theme
def find_theme_word(theme):
    exit_theme_words=load_theme_words()#存在文件的从train.xlsx文件提取的主题
    theme_words=[]
    for line in theme:
        temp = str(line).split()
        tt = ""
        for ii in temp:
            if ii in exit_theme_words:
                tt=tt+ii+";"
        theme_words.append(tt)
    return theme_words
#从情感字典中找到情感词所对应的情感倾向
def find_sentiment_words(sentiment):
    exit_sentiment_words=load_sentiment_words()
    sentiment_words=[]
    sentiment_anls=[]
    for line in sentiment:
        temp = str(line).split()
        #print("temp:",temp)
        sw = ""
        sa=""
        for ii in temp:
            if ii in exit_sentiment_words:
                sw=sw+ii + ";"
                sa=sa+exit_sentiment_words[ii] + ";"
        sentiment_words.append(sw)
        sentiment_anls.append(sa)
    # file = open('words.txt', 'w')
    # file.write(str(sentiment_words))
    # file.close()
    # file = open('anls.txt', 'w')
    # file.write(str(sentiment_anls))
    # file.close()
    return sentiment_words,sentiment_anls

def result_write(theme_words,sentiment_word,sentiment_anls):
    file_object = open("data/output.csv", 'w', encoding='UTF-8')
    for w in range(len(test)):
        ss = ""
        if test.loc[w, 'row_id'] == "":
            ss = ss + ""
        else:
            ss = ss + str(test.loc[w, 'row_id']) + ","
        if test.loc[w, 'content'] == "":
            ss = ss + ""
        else:
            ss = ss + str(test.loc[w, 'content']) + ","
        ss = ss + str(theme_words[w]) + ","
        ss = ss + str(sentiment_word[w]) + ","
        ss = ss + str(sentiment_anls[w])
        # print("ss:",ss)
        file_object.write(ss + "\n")
    file_object.close()
    print("write finish!!!")

test = pd.read_csv('data/test.csv',header=None,names=['row_id','content'])
#jieba.load_userdict('data/sentiment_words.txt')
jieba.load_userdict('data/theme_words.txt')
jieba.load_userdict('data/sentiment_words.txt')
analyse.set_stop_words("data/stopwords.txt")
exit_theme_words = load_theme_words()
exit_sentiment_words=load_sentiment_words()
def deal(sentence):
    # sentence_seged = jieba.cut(sentence)
    # stopwords = analysis.stopwordslist('data/stopwords.txt')  # 这里加载停用词的路径
    # outstr = ''
    # for word in sentence_seged:
    #     if word not in stopwords:
    #         if word != '\t':
    #             outstr += word
    #             outstr += ""
    lines = str(sentence).split(' ')
    theme_words=[]
    sentiment_word=[]
    sentiment_value=[]
    isUsed={} #用来记录ss在索引i或者j出的词是否被用过
    for i in lines:
        isUsed[i]=0
    for i in range(len(lines)):
        if isUsed[lines[i]]==0 and lines[i] in exit_sentiment_words.keys():
            isUsed[lines[i]]=1
            sentiment_word.append(lines[i])
            sentiment_value.append(exit_sentiment_words[lines[i]])
            flag = 0
            for j in range(0,i):
                if isUsed[lines[i-j-1]]==0 and lines[i-j-1] in exit_theme_words:
                    theme_words.append(lines[i-j-1])
                    isUsed[lines[i-j-1]]=1
                    flag=1
            if flag==0:
                theme_words.append('NULL')
    tt=""
    for i in range(len(theme_words)):
        tt+=theme_words[i]+";"
    tt+=','
    for i in range(len(sentiment_word)):
        tt+=sentiment_word[i]+";"
    tt += ','
    for i in range(len(sentiment_value)):
        tt+=sentiment_value[i]+";"
    #print(tt)
    return tt

content = test['content'].apply(analysis.seg_stopword_sentence)#做停用词处理
result=[]
file_object = open("data/output.csv", 'w', encoding='UTF-8')
for i in range(len(content)):
    tmp = ""
    if test.loc[i, 'row_id'] == "":
        tmp = tmp + ""
    else:
        tmp = tmp + str(test.loc[i, 'row_id']) + ","
    if test.loc[i, 'content'] == "":
        tmp = tmp + ""
    else:
        tmp = tmp + str(test.loc[i, 'content']) + ","
    tmp+=deal(content[i])
    print(tmp)
    #result.append(tmp)
    file_object.write(tmp + "\n")
file_object.close()
print("write finish!!!")

# theme_words = find_theme_word(content)
# sentiment_word,sentiment_anls = find_sentiment_words(content)
# result_write(theme_words,sentiment_word,sentiment_anls)
