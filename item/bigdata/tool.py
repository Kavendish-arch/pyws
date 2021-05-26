from os import times
import random
import shelve
from contextlib import closing
from operator import itemgetter
import logging
import numpy as np


# read file
def load_file(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                # 去掉文件第一行的title
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)


def get_dataset(filename, pivot=0.75):
    trainSet = {}
    testSet = {}
    trainSet_len = 0
    testSet_len = 0
    # 加载文件， 按行读取
    for line in load_file(filename):
        # 读取列属性
        user, movie, rating, timestamp = line.split(',')
        # 数据划分测试集合和数据集合 (0,1) < (0,pivot)
        if random.random() < pivot:
            trainSet.setdefault(user, {})
            trainSet[user][movie] = rating
            trainSet_len += 1
        else:
            testSet.setdefault(user, {})
            testSet[user][movie] = rating
            testSet_len += 1
    print('Split trainingSet and testSet success!')
    print('TrainSet = %s' % trainSet_len)
    print('TestSet = %s' % testSet_len)
    return trainSet, testSet

# 保存为csv
def save_as_csv(item, f_name):
    """
    item: 代保存的数据
    f_name: 文件路径
    """
    ii = 0
    with open(f_name, 'a') as rf:
        for i, score in item.items():
            # 写入表头
            if ii == 0:
                try:
                    for key in score.keys():
                        rf.write(',%s' % key)
                except AttributeError:
                    continue
                ii += 1
                rf.write('\n')
            # 写入key
            rf.write('%s' % i)
            try:
                for value in score.values():
                    rf.write(',%s' % value)
                rf.write('\n')
            except AttributeError:
                continue


# 保存为shelve
def save_as_shelve(keys, item, f_name):
    """
    item: 保存的文件
    f_name: 文件名
    """
    with closing(shelve.open(f_name, 'c')) as sh:
        for i in item.keys():
            sh[i] = item.get(i)


def jacard(movie_popular, movie_sim_matrix):
    print("Calculating movie similarity matrix ...")
    print('Calculate movie similarity matrix success!')

    
class Similarity(object):
    '''
        相似度算法工具类
    '''
    try:
        import numpy as np
    except ImportError:
        logging.error("import numpy error, please install numpy")

    def eucledian_distance(self, x, y):
        """欧氏距离"""
        return np.sqrt(np.sum(np.power(np.array(x) - np.array(y), 2)))

    def manhattan_distance(self, x, y):
        """曼哈顿距离"""
        # xy = np.abs(x - y)
        return np.sum(np.abs(np.array(x) - np.array(y)))

    def minkowski_distance(self, x,y,n):
        """闵可夫斯基距离"""
        return np.power(np.sum(np.power(np.array(x) - np.array(y), n)), 1/n)

    def chebyshev_distance(self, x, y):
        '''切比雪夫距离'''
        return np.max(np.abs(np.array(x) - np.array(y)))

    def cosine_similarity(self, x, y):
        return np.dot(x, y) / \
               (np.linalg.norm(x, 2) * np.linalg.norm(y, 2))

    def jaccard_similarity(self, x, y):
        a = set.intersection(set(x), set(y))
        b = set.union(*[set(x), set(y)])
        return len(a) / len(b)

    def jaccard_distance(self, x, y):
        """jaccard 距离 1- jaccard 系数"""
        a = set.intersection(set(x), set(y))
        b = set.union(*[set(x), set(y)])
        return 1 - len(a) / len(b)

    def tanimoto_similarity(self, x, y):
        """tanimoto 系数 广义jaccard 系数"""
        xy = np.dot(x, y)
        x = np.linalg.norm(x, 2)
        y = np.linalg.norm(y, 2)
        return xy / (x + y - xy)
    def RMSE(self, y1,y2):
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
        y1, y2 = np.array(y1), np.array(y2)
        return np.sqrt(np.sum(np.power(y1 - y2, 2))/len(y1))

    def MAE(self, y1, y2):
        '''
        >>> a = [1,2,3]
        >>> b = [2,3,5]
        >>> MAE(a,b)
        1.1547005383792515
        '''

        if len(y1) != len(y2):
            return -1
        y1, y2 = np.array(y1), np.array(y2)
        return np.sqrt(np.sum(np.abs(y1 - y2))/len(y1))


if __name__ == "__main__":
    path = '..\\file\\ratings.csv'
    # trainSet, testSet = get_dataset(path)

    sim = Similarity()
    a = [1,2,3]
    b = [2,3,5]

    print(sim.RMSE(a, b))
    sim.hell0()