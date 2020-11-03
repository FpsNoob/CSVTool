# 使用词袋模型提取出文本关键字
import pandas as pd
import codecs
import train_bagmodel as td

def extract(question, stop_key):
    question = td.data_prepos(question[0], stop_key)
    keywords = []
    point = []
    df = pd.read_csv("./result/point_keywords.csv", encoding='utf-8')
    for i in range(len(df['keywords'])):
        for j in question:
            if j == df['keywords'][i] and j not in keywords:
                keywords.append(j)
                if df['point'][i] not in point:
                    point.append(df['point'][i])
    return keywords, point


# def get_question(point):





if __name__ == '__main__':
    stop_key = [w.strip() for w in codecs.open('./list/stopWord.txt', 'r', encoding='utf-8').readlines()]
    f = open('question.txt', 'r',  encoding='utf-8')
    question = f.readlines()
    #print(question)
    keywords, point = extract(question, stop_key)
    print(keywords)
    print(point)
