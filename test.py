import pandas as pd
import analysis
import jieba

#加载主题词典
def load_theme_words(filepath='data/theme_words.txt'):
    theme_words = [line.strip() for line in open(filepath, 'r', encoding='utf-8').readlines()]
    return theme_words

#加载情感词典
def load_sentiment_words(filepath='data/sentiment_words_正负面.txt'):
    theme_words={}
    for line in open(filepath, 'r', encoding='utf-8').readlines():
        tt = line.split()
        print("tt[0]:",tt[0],"tt[1]:",tt[1])
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



test = pd.read_csv('data/test.csv',header=None,names=['row_id','content'])
#jieba.load_userdict('data/sentiment_words.txt')
jieba.load_userdict('data/theme_words.txt')
theme = test['content'].apply(analysis.seg_sentence)
theme_words = find_theme_word(theme)
sentiment_word,sentiment_anls = find_sentiment_words(theme)

file_object = open("data/output.csv", 'w', encoding='UTF-8')
for w in range(len(test)):
    ss=""
    if test.loc[w,'row_id']=="":
        ss = ss+""
    else:
        ss = ss+str(test.loc[w,'row_id'])+","
    if test.loc[w,'content']=="":
        ss = ss+""
    else:
        ss=ss+str(test.loc[w,'content'])+","
    ss =ss+str(theme_words[w])+","
    ss=ss+str(sentiment_word[w])+","
    ss=ss+str(sentiment_anls[w])
    #print("ss:",ss)
    file_object.write(ss+"\n")
file_object.close()
print("write finish!!!")