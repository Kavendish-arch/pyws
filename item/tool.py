import os
import random
import csv
import numpy as np
# yield 加载文件


def load_file(filename):
    """open file load data"""
    i = -1
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        # for i, line in enumerate(f):
        for row in reader:
            i += 1
            if i == 0:
                # 去掉文件第一行的title
                continue
            yield row
    print('Load %s success! count %d records' % (filename,i))


    # 读文件，返回文件的每一行
def load_file_2(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                # 去掉文件第一行的title
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)


def random_list(len_l, max_limit, func):
    data_r = []
    for _ in range(len_l):
        data_r.append(func(max_limit))
    return data_r


def random_num(max_limit):
    return random.random() * max_limit


def random_int(max_limit):
    return round(random.random() * max_limit)


def RMSE(y1,y2):
    '''
    :param y1:
    :param y2:
    :return:
    >>> a = [1,2,3]
    >>> b = [2,3,5]
    >>> print(RMSE(a,b))
    1.4142135623730951
    '''
    if len(y1) != len(y2):
        return -1
    tmp = np.sum(np.subtract(y1,y2) ** 2)
    tmp = np.sqrt(tmp/len(y1))
    return tmp


def MAE(y1, y2):
    '''
    :param y1:
    :param y2:
    :return: MAE 均方误差
    >>> a = [1,2,3]
    >>> b = [2,3,5]
    >>> MAE(a,b)
    1.1547005383792515
    '''
    if len(y1) != len(y2):
        return -1
    tmp = np.sum(np.abs(np.subtract(y1,y2)))
    tmp = np.sqrt(tmp/len(y1))
    return tmp


def precision_recall(y1, y2):
    '''
    :param y1:  推荐的
    :param y2:  用户喜欢的
    :return:    准确率
    '''
    hit = []
    for i in y1:
        if i in y2:
            hit.append(i)
    precision = len(hit) / len(y1)
    recall = len(hit) / len(y2)
    return precision, recall


def f1_core(y1,y2):
    p,r = precision_recall(y1,y2)
    return {'f1':2 * p * r / (p + r), "precision":p,"recall":r}


if __name__ == "__main__":
    path = os.path.abspath(os.curdir) + \
           "\\bigdata\\ml-latest-small\\movies.csv"

    data = {}
    for line in load_file(path):
        movie_id, title = line[0], line[1:]
        data.setdefault(movie_id, title)
    # print(data)
    import doctest
    # doctest.testmod(verbose=True)


