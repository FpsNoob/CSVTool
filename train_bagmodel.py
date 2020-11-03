# 采用TF-IDF的方法提取题目中的关键字, 并生成一个词袋模型
import pandas as pd
import numpy as np
import codecs
import jieba.posseg
import jieba.analyse
import joblib
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer

# 显示字典中的映射关系
def display_dict(dict):
    for i in dict.keys():
        print('+++++++++++++++++++++++++++++++++++')
        print('key is %s'% i)
        print(dict[i])


def get_data(filePath):
    df = pd.read_csv(filePath, encoding='utf-8')
    data_len = len(df['point_123'])
    my_dict = {df['point_123'][i]: "" for i in range(data_len)}  # 将所有的point作为key添加到字典中
    for i in range(data_len):   # 遍历所有题目
        set_index = df['point_123'][i]
        question = df['question'][i]
        # print(question)
        my_dict[set_index] += question   # 合并有相同知识点的题目
    # display_dict(my_dict)
    return my_dict


def data_prepos(text, stop_key):
    l = []
    pos = ['n', 'nz', 'v', 'vd', 'vn', 'l', 'a', 'd']  # 定义选取的词性
    seg = jieba.posseg.cut(text)    # 分词
    for i in seg:
        if i.word not in stop_key and i.flag in pos:  # 去停用词 + 词性筛选
            l.append(i.word)
    return l

# 提取关键词
def tf_idf(point, question,  stop_key, topK):
    corpus = []
    keys = []
    for index in range(len(point)):
        print(index)
        text = data_prepos(question[index], stop_key)
        text = " ".join(text)   # 连接成字符串
        corpus.append(text)
    # 构建词频矩阵
    vectorizer = CountVectorizer()
    # a[i][j]:表示j词在第i个文本中的词频
    X = vectorizer.fit_transform(corpus)
    # 统计每个词的权值
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)
    # 保存词袋模型
    joblib.dump(transformer, 'model/word_bag.dict')
    # 获取关键词
    word = vectorizer.get_feature_names()
    # 获取tf-idf矩阵，a[i][j]表示j词在i篇文本中的tf-idf权重
    weight = tfidf.toarray()
    for i in range(len(weight)):
        print("-------这里输出第", i + 1, u"篇文本的词语tf-idf------")
        df_word, df_weight = [], []
        for j in range(len(word)):
            print(word[j], weight[i][j])
            df_word.append(word[j])
            df_weight.append(weight[i][j])
        df_word = pd.DataFrame(df_word, columns=['word'])
        df_weight = pd.DataFrame(df_weight, columns=['weight'])
        word_weight = pd.concat([df_word, df_weight], axis=1)  # 拼接词汇列表和权重列表
        word_weight = word_weight.sort_values(by="weight", ascending=False)  # 按照权重值降序排列
        keyword = np.array(word_weight['word'])  # 选择词汇列并转成数组格式
        word_split = [keyword[x] for x in range(0, topK)]  # 抽取前topK个词汇作为关键词
        # print(word_split)
        word_split = ",".join(word_split)
        # print(word_split)
        keys.append(word_split)
    result = pd.DataFrame({"point": point, "key_words": keys}, columns=['point', 'key_words'])
    return result

def point_to_keywords(file_path):
    df = pd.read_csv(file_path, encoding='utf-8')
    point_keywords = []
    data_len = len(df['point'])
    for i in range(data_len):
        key_words = df['key_words'][i].split(',')
        for key in key_words:
            t = (df['point'][i], 'relation', key)
            print(t)
            point_keywords.append(t)
    df = pd.DataFrame(point_keywords, columns=['point', 'relation', 'keywords'])
    #df.to_csv('./result/point_keywords.csv', encoding='utf-8', index=0)


if __name__ == "__main__":
    filePath = r'./data/point_stem.csv'
    point_dict = get_data(filePath)  # 合并有相同知识点的题目
    # 加载停用词
    stop_key = [w.strip() for w in codecs.open('./list/stopWord.txt', 'r', encoding='utf-8').readlines()]
    # 对每个知识点所对应的题目进行关键词提取
    point = []
    question = []
    for p in point_dict.keys(): # 从dict中取出知识点和题目
        point.append(p)
        question.append(point_dict[p])
    result = tf_idf(point, question, stop_key, 10)
    # result.to_csv('./result/point_keywords.csv', encoding='utf-8', index=0)
   # point_to_keywords('./result/高中生物.csv')


