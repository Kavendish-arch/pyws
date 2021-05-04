# coding = utf-8

# 基于用户的协同过滤推荐算法实现
from contextlib import closing
from datetime import datetime
import shelve
from util import tool
from operator import itemgetter


class UserBasedCF():
    # 初始化相关参数
    def __init__(self):
        # 找到与目标用户兴趣相似的20个用户，为其推荐10部电影
        self.n_sim_user = 20
        self.n_rec_movie = 10

        # 将数据集划分为训练集和测试集
        self.trainSet = {}
        self.testSet = {}

        # 用户相似度矩阵
        self.user_sim_matrix = {}
        self.movie_count = 0

        self.evaluates = {}

        print('Similar user number = %d' % self.n_sim_user)
        print('Recommneded movie number = %d' % self.n_rec_movie)

    # 读文件得到“用户-电影”数据 ,分为测试集和训练集
    def init_dataset(self, filename,):
        self.trainSet, self.testSet = tool.get_dataset(filename)

    # 计算用户之间的相似度
    def calc_user_sim(self):
        # 构建“电影-用户”倒排索引
        # key = movieID, value = list of userIDs who have seen this movie
        print('Building movie-user table ...')
        movie_user = {}
        for user, movies in self.trainSet.items():
            for movie in movies:
                if movie not in movie_user:
                    movie_user[movie] = set()
                movie_user[movie].add(user)
        print('Build movie-user table success!')

        self.movie_count = len(movie_user)
        print('Total movie number = %d' % self.movie_count)

        print('Build user co-rated movies matrix ...')
        # user-user 矩阵
        for movie, users in movie_user.items():
            for u in users:
                for v in users:
                    if u == v:
                        continue
                    self.user_sim_matrix.setdefault(u, {})
                    self.user_sim_matrix[u].setdefault(v, 0)
                    self.user_sim_matrix[u][v] += 1
        print('Build user co-rated movies matrix success!')

        # 计算相似性, 用户之间得相似性
        print('Calculating user similarity matrix ...')
        for u, related_users in self.user_sim_matrix.items():
            for v, count in related_users.items():
                self.user_sim_matrix[u][v] = count \
                    / (len(self.trainSet[u]) + len(self.trainSet[v]) - count)

                # self.user_sim_matrix[u][v] = count / math.sqrt(len(self.trainSet[u]) * len(self.trainSet[v]))
        print('Calculate user similarity matrix success!')

    # 针对目标用户U，找到其最相似的K个用户，产生N个推荐
    def recommend(self, user):
        K = self.n_sim_user
        N = self.n_rec_movie
        rank = {}
        watched_movies = self.trainSet[user]

        # v=similar user, wuv=similar factor
        for v, wuv in sorted(self.user_sim_matrix[user].items(),
            key=itemgetter(1), reverse=True)[0:K]:
            for movie in self.trainSet[v]:
                if movie in watched_movies:
                    continue
                rank.setdefault(movie, 0)
                rank[movie] += wuv
        return sorted(rank.items(), key=itemgetter(1), reverse=True)[0:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print("Evaluation start ...")
        N = self.n_rec_movie
        # 准确率和召回率 hit 命中数、rec_count 推荐数、test_count 结果数目
        hit = 0
        rec_count = 0
        test_count = 0
        # 覆盖率, 总推荐电影清单
        all_rec_movies = set()

        for i, user, in enumerate(self.trainSet):
            user_hit = 0
            user_evaluate = {}

            test_movies = self.testSet.get(user, {})
            rec_movies = self.recommend(user)
            user_evaluate.setdefault("train_len", len(self.trainSet.get(user)))
            user_evaluate.setdefault("test_len", len(test_movies))
            user_evaluate.setdefault("rec_len", len(rec_movies))

            # 准确率
            for movie, w in rec_movies:
                if movie in test_movies:
                    user_hit += 1
                all_rec_movies.add(movie)

            user_evaluate.setdefault('hit', user_hit)

            x = len(rec_movies)
            y = len(test_movies)
            # 每个用户的 f1 score
            user_precision = 0 if x == 0 else user_hit / x
            user_evaluate.setdefault('precision', user_precision)

            user_recall = 0 if y == 0 else user_hit / y
            user_evaluate.setdefault('recall', user_recall)

            # f1 score
            f1_score = -1 \
                if user_recall + user_precision == 0 \
                else 2 * user_precision * user_recall \
                           / (user_recall + user_precision)
            user_evaluate.setdefault('f1_score', f1_score)

            self.evaluates.setdefault(user, user_evaluate)
            # 命中数
            hit += user_hit
            # 推荐的个数
            rec_count += N
            # 结果的个数
            test_count += len(test_movies)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)  #
        coverage = len(all_rec_movies) / (1.0 * self.movie_count)

        self.evaluates.setdefault('all_hit',hit)
        self.evaluates.setdefault('precision',precision)
        self.evaluates.setdefault('recall', recall)
        self.evaluates.setdefault('rec_count', rec_count)
        self.evaluates.setdefault('res_count', test_count)
        self.evaluates.setdefault('coverage', coverage)


if __name__ == '__main__':
    rating_file = 'ratings.csv'
    userCF = UserBasedCF()
    userCF.init_dataset(rating_file)
    a = datetime.now()
    userCF.calc_user_sim()
    b = datetime.now()
    userCF.evaluates.setdefault("method_calc_movie_sim_2",
                        (b-a).seconds)
    userCF.evaluate()

    tool.save_as_csv(userCF, "..\\csv\\userCF_2_3.csv")
    tool.save_as_shelve(userCF.evaluates.keys(),
                        userCF.evaluates , '..\\data\\userCF_2_3.data')


def tmp():
    tmp = {}
    with closing(shelve.open('time1.data', 'r')) as she:
        tmp = she['time1']
    # print(tmp)
    path = 'result_1.csv'
    evaluates = {}
    with open(path,'w') as file:
        ii = 0
        for i,item in tmp.items():
            if ii == 0:
                for key in item.keys():
                    file.write(', %s'%key)
                file.write('\n')
                ii = 1
            file.write('%s '%(i))
            try:
                tmp_list = tmp.get(i).values()
            except:
                continue
            for value in tmp_list:
                file.write(' ,%s ' % value)
            file.write("\n")

