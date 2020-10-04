import os
import pandas as pd
import numpy as np
import datetime
import re
from tensorflow.python.platform import gfile


def depart_data(filepath, filename, lines):
    '''
    保存切分文件在depart文件夹中
    :param filepath: csv文件的目录
    :param filename: 文件名
    :param lines: 切分成包含lines行数据的小文件
    '''
    filepath = os.path.join(path, filename + '.csv')
    with open(filepath, 'r', encoding='utf-8') as f:
        csvfile = f.readlines()
    filecnt = 1
    for i in range(0, len(csvfile), lines):
        savepath = os.path.join(path, 'depart', filename + '_' + str(filecnt) + '.csv')
        print(savepath)
        with open(savepath, 'w+', encoding='utf-8') as f:
            if filecnt > 1:
                f.write(csvfile[0])
                print('save data')
            f.writelines(csvfile[i:i + lines])
        filecnt += 1
    f.close()


def filter_data(path, file_format):
    '''
    取数据中所需要的属性，并且去除错误行
    :param path:  文件夹目录
    :param file_format: 文件类型
    :return:
    '''
    search_path = os.path.join(path, 'depart', file_format)
    for file_path in gfile.Glob(search_path):
        try:
            print('load file: %s' % file_path)
            fd = pd.read_csv(file_path, encoding='utf-8', usecols=['subject', 'points', 'points_2', 'points_3',
                                                                   'stem_search', 'stem_html'], error_bad_lines=False)
            filename = os.path.basename(file_path)
            save_path = os.path.join(path, 'filter', filename)
            print('save data：%s' % filename)
            fd.to_csv(save_path, index=False, encoding='utf-8')
        except Exception as e:
            print("pandas.errors.ParserError : " + str(e))
            pass


def combine(path, file_format):
    '''
    将数据按照学科分类，
    :param path:
    :param file_format:
    :return:
    '''
    print('按学科来区分题目.....')
    subject_list = []
    search_path = os.path.join(path, 'filter', file_format)
    for file_path in gfile.Glob(search_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            groups = df.groupby(df['subject'])
            for group in groups:
                mark = re.sub("\D", "", file_path)
                subject_name = str(group[0])
                if subject_name not in subject_list:
                    subject_list.append(subject_name)
                    print(subject_name)
                # group[1].to_csv(path+"/combine/" + mark + str(group[0]) + ".csv", index=False, encoding='utf-8')
        except Exception as e:
            pass
    return subject_list


def final(path):
    subjectList = loadSubjectName()
    searchPath = os.path.join(path, 'combine')
    for subjectName in subjectList:
        savePath = os.path.join(path, 'final', subjectName + '.csv')
        with open (savePath ,'w+', encoding='utf-8') as f:
            cnt = 0
            print(u"开始合并%s..." % (subjectName))
            file_list = os.listdir(searchPath)
            for file in file_list:
                name = os.path.splitext(file)[0]
                name = re.sub("\d", "", name)
                if name == subjectName:
                    cnt += 1
                    print(file)
                    csvfile = open(searchPath + '\\' + file, 'r', encoding='utf-8')
                    for i in csvfile.readlines():
                        f.write(i)
            print("合并结束，共%d个文件" % cnt)

def saveSubjectName(subjectList):
    f = open('./subject_list.txt', 'w')
    for subject_name in subjectList:
        isdigit = re.search(r'\d', subject_name)
        if isdigit is None:
            f.write(subject_name)
            f.write('\n')
    f.close()

def loadSubjectName():
    subject_list = []
    f = open('./subject_list.txt', 'r')
    for i in f.readlines():
        i = ''.join(i).strip('\n')
        subject_list.append(i)
    return subject_list



def str_deal(str1, str2, str3, all_point):
    str1 = jud(str1)
    str2 = jud(str2)
    str3 = jud(str3)
    all_point += str1+str2+str3
    all_point = re.sub(r'[、]', ',', all_point)
    return all_point



def jud(p):
    if pd.isnull(p):
        p = ""
    else:
        if type(p) == type("str"):
            p = p+','
        else:
            p = str(p)+','
    return p

def string_duplicate_4(s):
    new_s = []
    for x in s:
        if x not in new_s:
            if x!='':
                new_s.append(x)
    return new_s


def duplication(filepath, name):
    duplicate = []
    r = '[a-zA-Z0-9’.!"#$%&\'()*+,-./:；;<=>?@[\\]^_`{|}~\n。！，]'
    df = pd.read_csv(filepath, encoding='utf-8')
    for stem in df['stem_search']:  # 将题目进行去标点符号字符等等，用于题目去重
        stem = stem.replace(" ", "")
        stem = re.sub(r, '', stem)
        duplicate.append(stem)
        #print(stem)
    df['duplicate'] = duplicate
    data_len = len(df['duplicate'])
    point = []
    for i in range(data_len):  # 将相同题目的知识点合并，使用逗号隔开知识点，存于point属性中
        stem_base = df['duplicate'][i]
        all_point = ""
        for j in range(i, data_len, 1):
            print('in %d : %d'%(i, j))
            p1 = df['points'][j]
            p2 = df['points_2'][j]
            p3 = df['points_3'][j]
            if df['duplicate'][j] == stem_base:
                all_point = str_deal(p1, p2, p3, all_point)
        point.append(all_point)
    print(len(point))
    df['point'] = point
    print('-----------------------')
    print(len(df['point']))
    df = df.drop_duplicates(subset='duplicate', keep='first', inplace=False)  # 保存中间数据，以免出现bug后。。。
    data_len = len(df['point'])
    df.to_csv('./'+name, columns=['point', 'stem_search', 'stem_html'],
              encoding='utf-8', index=0)
    df = pd.read_csv('./test_'+name, encoding='utf-8')
    points = []
    question = []
    data_len = len(df['point'])
    question_html = []
    for i in range(data_len):
        print(i)
        str = df['point'][i]
        if pd.isnull(str):
            continue
        else:
            # print(str)
            str = str.split(',')
            str = string_duplicate_4(str)
            if str=='':
                break
            else:
                for x in str:
                    points.append(x)
                    question.append(df['stem_search'][i])
                    question_html.append(df['stem_html'][i])
    final_csv = []
    for i in range(len(points)):
        t = (points[i], question[i], question_html[i])
        final_csv.append(t)
    final_df = pd.DataFrame(final_csv, columns=['point_123','question','question_html'])
    final_df.drop_duplicates()
    final_df.to_csv('./'+name, encoding='utf-8', index=0)


if __name__ == '__main__':
    path = 'D:\WorkSpace\错题推荐\Data\csv_data\高中学科'
    fileName = '高中生物.csv'
    file_path = os.path.join(path, fileName)
    duplication(file_path, fileName)
    lines = 5000
    fileFormat = '*.csv'
    # slipt_data(path, file_name, lines)
    # filter_data(path, '*.csv')
    # subjectList = combine(path, '*.csv')
    # saveSubjectName(subjectList)
    #final(path)
