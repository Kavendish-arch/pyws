# ItemCF 协同过滤算法

import os 
import random
import math
from operator import itemgetter
import tool
class ItemCF(object):

    def __init__(self):
        self.trainSet = {}
        self.testSet = {}
        self.trainSet_len = 0
        self.testSet_len = 0
        
        self.movie_sim_matrix = {}
        self.movie_popular = {}


    def initData(self, path):
        # read file
        self.trainSet, self.testSet = tool.get_dataset(path)
    
    def count_movie(self):
        # 统计电影的播放次数，movie_movie 矩阵
        # 统计电影被看的次数
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in self.movie_popular:
                    self.movie_popular[movie] = 0
                self.movie_popular[movie] += 1
        print("Total movie number = %d" % len(self.movie_popular))
    
    def create_movie_movie_matrix(self):
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

    
    # 计算电影之间的相似度 相似度算法 AB交集 / 根号下(A*B)
    def calc_movie_sim(self):
        # 计算电影之间的相似性
        print("Calculating movie similarity matrix ...")
        for m1, related_movies in self.movie_sim_matrix.items():
            for m2, count in related_movies.items():
                # 注意0向量的处理，即某电影的用户数为0
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                else:
                    self.movie_sim_matrix[m1][m2] = count / math.sqrt(self.movie_popular[m1] * self.movie_popular[m2])
        print('Calculate movie similarity matrix success!')

    # 计算电影之间的相似度, jacard 算法 交集/并集
    def calc_movie_sim_jacard(self):
        # 计算电影之间的相似性
        print("Calculating movie similarity matrix ...")
        for m1, related_movies in self.movie_sim_matrix.items():
            for m2, count in related_movies.items():
                # 注意0向量的处理，即某电影的用户数为0
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                else:
                    self.movie_sim_matrix[m1][m2] = count / (self.movie_popular[m1] + self.movie_popular[m2] -count)
        # jacard = (交集)/(并集)
        print('Calculate movie similarity matrix success!')


    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
    # 用户未产生过行为的物品
    def recommend(self, user_id):
    #  user, n_sim_movie, n_rec_movie, trainSet, movie_sim_matrix):
        K = n_sim_movie
        N = n_rec_movie
        # 用户user对物品的偏好值
        self.rank = {}
        # 用户user产生过行为的物品，与物品item按相似度从大到小排列，取与物品item相似度最大的k个商品
        # 验证是否有用户的历史记录
        if user_id in trainSet:
            pass
        else:
            print("use other method to recommend !")
        try:
            watched_movies = trainSet[user_id]
        except KeyError:
            print(user + " is not exits")

        for movie, rating in watched_movies.items():
            # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
            for related_movie, w in sorted(self.movie_sim_matrix[movie].items(), key=itemgetter(1), reverse=True)[:K]:
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
            test_moives = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            for movie, w in rec_movies:
                if movie in test_moives:
                    hit += 1
                all_rec_movies.add(movie)
            rec_count += N
            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)
        print('precisioin=%.4f\trecall=%.4f\tcoverage=%.4f' % (
            precision, recall, coverage))


from datetime import datetime

if __name__ == "__main__":
    time_count = {}

    item = ItemCF()
    path = 'ratings.csv'

    # read_file
    a = datetime.now()
    item.initData(path)
    b = datetime.now()
    time_count.setdefault("read_file_time",b-a)
    print((b-a).seconds)
    
    a = datetime.now()
    item.count_movie()
    b = datetime.now()
    time_count.setdefault("create_movie_popular",b-a)
    print((b-a).seconds)
    
    a = datetime.now()
    item.create_movie_movie_matrix()
    b = datetime.now()
    time_count.setdefault("create_movie_movie_matrix",b-a)
    print((b-a).seconds)
    
    a = datetime.now()
    item.calc_movie_sim()
    b = datetime.now()
    print((b-a).seconds)
    time_count.setdefault("method_calc_movie_sim_1",b-a)

    a = datetime.now()
    item.calc_movie_sim_jacard()
    b = datetime.now()
    print((b-a).seconds)
    time_count.setdefault("method_calc_movie_sim_2",b-a)

    print(time_count)