# ItemCF 协同过滤算法, 不同相似性算法

import math
from datetime import datetime
from util import tool as tool


class ItemCF(object):
    def __init__(self):
        self.trainSet = {}
        self.testSet = {}
        self.trainSet_len = 0
        self.testSet_len = 0

        self.movie_sim_matrix = {}
        self.movie_popular = {}

        self.evaluates = {}

        # 推荐相似电影：
        self.n_sim_movie = 20
        self.n_rec_movie = 20

    def initData(self, path):
        # read file
        self.trainSet, self.testSet = tool.get_dataset(path)

    def create_movie_movie_matrix(self):
        # 建立 movie movie 矩阵
        # 统计电影的播放次数，movie_movie 矩阵
        self.movie_popular, self.movie_sim_matrix \
            = tool.build_movie_matrix(self.trainSet)
        print("Total movie number = %d" % len(self.movie_popular))
        print("Build 同现矩阵co-rated users matrix success!")

    # 计算电影之间的相似度 相似度算法 AB交集 / 根号下(A*B)
    def calc_movie_sim(self):
        # 改进的jacard 算法， 计算电影之间的相似性
        print("Calculating movie similarity matrix ...")
        for m1, related_movies in self.movie_sim_matrix.items():
            for m2, count in related_movies.items():
                # 注意0向量的处理，即某电影的用户数为0
                if self.movie_popular[m1] == 0 or self.movie_popular[m2] == 0:
                    self.movie_sim_matrix[m1][m2] = 0
                else:
                    self.movie_sim_matrix[m1][m2] \
                        = count / math.sqrt(self.movie_popular[m1]
                                            * self.movie_popular[m2])
        print('Calculate movie similarity matrix success!')

    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
    # 用户未产生过行为的物品
    def recommend(self, user_id):
        # 用户user对物品的偏好值
        # self.rank = tool.recommend(aim=self, user_id=user_id)
        pass

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        tool.evaluate(self)


if __name__ == "__main__":
    # 记录时间信息

    item = ItemCF()
    path = 'ratings.csv'

    # read_file
    item.initData(path)

    a = datetime.now()
    # 建立同现矩阵
    item.create_movie_movie_matrix()
    item.calc_movie_sim()
    b = datetime.now()
    item.evaluates.setdefault("method_calc_movie_sim_2", b - a)

    a = datetime.now()
    item.evaluate()
    b = datetime.now()
    item.evaluates.setdefault("method_evaluate", b - a)

    tool.save_as_csv(item, '..\\csv\\itemCF_2_3.csv')
    tool.save_as_shelve(['evaluates', 'method_calc_movie_sim_2',
                         'method_evaluate'],
                        item.evaluates, "..\\data\\itemCF_2_3.data")
