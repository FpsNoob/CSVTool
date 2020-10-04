# 采用TF-IDF的方法提取题目中的关键字
import sys
import pandas as pd
import numpy as np
import jieba.posseg
import jieba.analyse
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer


# 使用dict创建知识点和题目的映射关系
def questionPrepos(filePath):
    df = pd.read_csv(filePath, encoding='utf-8')
    data_len = len(df['point_123'])
    my_dict = {df['point_123'][i]: [] for i in range(data_len)}  # 将所有的point作为key添加到字典中
    for i in range(data_len):   # 添加value，point所对应的题目
        set_index = df['point_123'][i]
        question = df['question'][i]
        my_dict[set_index].append({'question': question})


if __name__ == "__main__":
    filePath = r'./高中物理.csv'
    questionPrepos(filePath)

