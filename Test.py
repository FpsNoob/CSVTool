import os
import pandas as pd
import csv
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


def dupilication():
    '''
    jfkfh sk
    :return:
    '''


if __name__ == '__main__':
    path = r'D:\WorkSpace\错题推荐\Data\csv_data'
    fileName = 't_xbj_record0930'
    lines = 5000
    fileFormat = '*.csv'
    # slipt_data(path, file_name, lines)
    # filter_data(path, '*.csv')
    # subjectList = combine(path, '*.csv')
    # saveSubjectName(subjectList)
    final(path)
