# coding = utf-8

# 基于项目的协同过滤推荐算法实现
import os
import random
import math
from operator import itemgetter
import shelve
from contextlib import closing
from item import Moive


class ItemBasedCF(object):

    # 初始化参数 构造方法
    def __init__(self):
        # 找到相似的20部电影，为目标用户推荐10部电影
        self.n_sim_movie = 20
        self.n_rec_movie = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度 矩阵
        self.movie_sim_matrix = {}
        # 电影-观看数统计
        self.movie_popular = {}
        self.movie_count = 0

        print('Similar movie number = %d' % self.n_sim_movie)
        print('Recommneded movie number = %d' % self.n_rec_movie)

    # 读文件，返回文件的每一行
    def load_file(self, filename):
        with open(filename, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i == 0:
                    # 去掉文件第一行的title
                    continue
                yield line.strip('\r\n')
        print('Load %s success!' % filename)

    # 读文件得到“用户-电影”数据
    def get_dataset(self, filename, pivot=0.75):

        trainSet_len = 0
        testSet_len = 0
        # 加载文件， 按行读取
        for line in self.load_file(filename):
            # 读取列属性
            user, movie, rating, timestamp = line.split(',')
            # 数据划分测试集合和数据集合 (0,1) < (0,pivot)
            if random.random() < pivot:
                self.trainSet.setdefault(user, {})
                self.trainSet[user][movie] = rating
                trainSet_len += 1
            else:
                self.testSet.setdefault(user, {})
                self.testSet[user][movie] = rating
                testSet_len += 1
        print('Split trainingSet and testSet success!')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

    def build_movie_matrix(self):
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                self.movie_popular[movie] += 1
        self.movie_count = len(self.movie_popular)
        print("Total movie number = %d" % self.movie_count)

        # 遍历训练数据，获得用户对有过的行为的物品
        for user, movies in self.trainSet.items():
            # 遍历该用户每件物品项
            for m1 in movies:
                # 遍历该用户每件物品项
                for m2 in movies:
                    # 若该项为当前物品，跳过
                    if m1 == m2:
                        continue
                    self.movie_sim_matrix.setdefault(m1, {})
                    self.movie_sim_matrix[m1].setdefault(m2, 0)
                    # 同一个用户，遍历到其他用品则加1
                    self.movie_sim_matrix[m1][m2] += 1
        print("Build 同现矩阵co-rated users matrix success!")

    # 计算电影之间的相似度
    def calc_movie_sim(self):
        # 计算电影之间的相似性
        print("Calculating movie similarity matrix ...")
        for m1, related_movies in self.movie_sim_matrix.items():
            for m2, count in related_movies.items():
                # 注意0向量的处理，即某电影的用户数为0
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                else:
                    # self.movie_sim_matrix[m1][m2] = count / math.sqrt(
                    #     self.movie_popular[m1] * self.movie_popular[m2])
                    self.movie_sim_matrix[m1][m2] = count /(
                        self.movie_popular[m1] + self.movie_popular[m2] - count)
        print('Calculate movie similarity matrix success!')

    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
    # 用户未产生过行为的物品
    def recommend(self, user):
        K = self.n_sim_movie
        N = self.n_rec_movie
        # 用户user对物品的偏好值
        rank = {}
        watched_movies = {}
        # 用户user产生过行为的物品，与物品item按相似度从大到小排列，取与物品item相似度最大的k个商品
        if user in self.trainSet:
            pass
        else:
            print("user other method")
        try:
            watched_movies = self.trainSet[user]
        except KeyError:
            print(user + " is not exits")

        for movie, rating in watched_movies.items():
            # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
            # if movie not in self.movie_sim_matrix:
                # continue
            for related_movie, w in \
                    sorted(self.movie_sim_matrix[movie].items(),
                           key=itemgetter(1), reverse=True)[:K]:
                # 若该物品为当前物品，跳过
                if related_movie in watched_movies:
                    continue
                # 计算用户user对related_movie的偏好值，初始化该值为0
                rank.setdefault(related_movie, 0)
                # 通过与其相似物品对物品related_movie的偏好值相乘并相加。
                # 排名的依据—— > 推荐电影与该已看电影的相似度(累计) * 用户对已看电影的评分
                rank[related_movie] += w * float(rating)
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):

        print('Evaluating start ...')
        N = self.n_rec_movie
        # 准确率和召回率
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率
        all_rec_movies = set()

        for i, user in enumerate(self.trainSet):
            # 测试集和 == 实际观看的
            test_moives = self.testSet.get(user, {})
            # 推荐集合 ==
            rec_movies = self.recommend(user)

            for movie, w in rec_movies:
                if movie in test_moives:
                    # 命中率
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (
            precision, recall, coverage))
        return (precision, recall, coverage)

    def save_data(self):
        with closing(shelve.open('temp_data', 'c')) as shelf:
            shelf['trainSet'] = self.trainSet
            shelf['testSet'] = self.testSet
            shelf['movie_popular'] = self.movie_popular
            shelf['movie_sim_matrix'] = self.movie_sim_matrix
            shelf['count'] = self.movie_count

    def read_data(self):
        with closing(shelve.open('temp_data', 'r')) as shelf:
            self.trainSet = shelf['trainSet']
            self.testSet = shelf['testSet']
            self.movie_popular = shelf['movie_popular']
            self.movie_sim_matrix = shelf['movie_sim_matrix']
            self.movie_count = shelf['count']

    # return list of users
    def get_user_List(self):
        name = []
        for user, _ in itemCF.trainSet.items():
            print(user)
            name.append(user)
        return name



if __name__ == '__main__':
    if os.path.exists("..\\file\\ratings.csv"):
        itemCF = ItemBasedCF()
        itemCF.get_dataset('..\\file\\ratings.csv')
        itemCF.build_movie_matrix()
        itemCF.calc_movie_sim()

    movie = Moive.MovieDetails()
    movie.get_movie_data('..\\file\\movies.csv')
    print('-'*10)

    list_item = itemCF.recommend('1')
    for movie_id, similar in list_item:
        print([movie_id, similar, movie.get_title(movie_id)])

