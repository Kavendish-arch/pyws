# coding = utf-8

# 基于项 的协同过滤推荐算法实现
import os
from operator import itemgetter
import shelve
from contextlib import closing
from user import Moive
from util import tool


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

    def initData(self, path):
        self.trainSet, self.testSet = tool.get_dataset(path)

    # 建立电影矩阵、 movie movie 矩阵
    def build_movie_matrix(self):
        self.movie_popular, self.movie_sim_matrix \
            = tool.build_movie_matrix(self.trainSet)

# 变化
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
        try:
            watched_movies = self.trainSet[user]
        except KeyError:
            print(user + " is not exits")

        for movie, rating in watched_movies.items():
            # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
            for related_movie, w in \
                    sorted(self.movie_sim_matrix[movie].items(),
                           key=itemgetter(1), reverse=True):
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

