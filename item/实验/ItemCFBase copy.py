# ItemCF 协同过滤算法
from datetime import datetime
from operator import itemgetter
import shelve
from contextlib import closing
import os
import tool 
import random

class ItemCF(object):

    def __init__(self):
        self.trainSet = {}
        self.testSet = {}
        self.trainSet_len = 0
        self.testSet_len = 0

        self.movie_sim_matrix = {}
        self.movie_popular = []

        self.evaluates = {}

        # 推荐相似电影：
        self.n_sim_movie = 20
        self.n_rec_movie = 20

    def initData(self, path):
        # read file
        # self.trainSet, self.testSet = tool.get_dataset(path)
        pass

    def get_dataset(self, filename, pivot=0.75):
        """
        movie-user 矩阵
        """
        trainSet = {}
        testSet = {}
        trainSet_len = 0
        testSet_len = 0
        # 加载文件， 按行读取
        for line in tool.load_file(filename):
            # 读取列属性
            user, movie, rating, _ = line.split(',')
            user = int(user)
            movie = int(movie)
            rating = float(rating)
            # 数据划分测试集合和数据集合 (0,1) < (0,pivot)
            if random.random() < pivot:
                trainSet.setdefault(movie, {})
                trainSet[movie][user] = rating
                trainSet_len += 1
            else:
                testSet.setdefault(movie, {})
                testSet[movie][user] = rating
                testSet_len += 1
        
        print('Split trainingSet and testSet success!')
        print('movie - user - matrix')
        print('TrainSet = %s' % trainSet_len)
        print('TestSet = %s' % testSet_len)

        self.trainSet = trainSet
        self.testSet = testSet
        self.testSet_len = testSet_len
        self.trainSet_len = trainSet_len
        return trainSet, testSet
    
    def count_user(self):
        trainSet = self.trainSet
        # 统计电影被看的次数
        movie_popular = []
        user_list = {}
        for movie, users in trainSet.items():
            if movie not in movie_popular:
                movie_popular.append(movie)
            for user in users:
                if user not in user_list:
                    user_list[user] = 0
                user_list[user] += 1

        print("Total user number = %d" % len(user_list))
        print("Total movie number = %d" % len(movie_popular))

        
        self.movie_popular = movie_popular
        self.user_list = user_list
        return movie_popular, user_list    

    # 
    def users_to_list(self):
        """
        方便相似度计算 
        movie 1,0,1,0,1,2               
        movie 2,1,2,0,0,0
        new_train 每个电影用户为定长数据
        """
        new_train = {}
        for movie, users in self.trainSet.items():
            new_user = []
            for i in self.user_list.keys():
                new_user.append(users.get(i, 0))
            new_train.setdefault(movie, new_user)
        self.new_trainSet = new_train


    def calc_movie_sim_cosine(self):
        # 计算电影之间的相似度
        sim = tool.Similarity()
        print("Calculating movie similarity matrix ...")
        i, max = 0, len(self.movie_popular)
        sorted(self.movie_popular)
        for m1 in self.movie_popular:
            self.movie_sim_matrix.setdefault(m1, {})
            for m2 in self.movie_popular:                    
                if m1 == m2:
                    self.movie_sim_matrix[m1].setdefault(m2, 1)
                    break

                # if m2 in self.movie_sim_matrix:
                    # self.movie_sim_matrix[m1][m2] = self.movie_sim_matrix[m2][m1]
                    # break

                u1 = self.new_trainSet.get(m1)
                u2 = self.new_trainSet.get(m2)

                if self.movie_sim_matrix[m1][m2] != 0:
                    self.movie_sim_matrix[m2][m1] = 
                simi = sim.cosine_similarity(u1,u2)

                self.movie_sim_matrix[m1].setdefault(m2, simi)
            i+=1
            print("\r{0}%".format(round(i/max*100,3)), end='')

        print('Calculate movie similarity matrix success!')

    # 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
    # 用户未产生过行为的物品
    def recommend(self, user_id):
        K = self.n_sim_movie
        N = self.n_rec_movie
        # 用户user对物品的偏好值
        self.rank = {}
        # 用户user产生过行为的物品，与物品item按相似度从大到小排列，取与物品item相似度最大的k个商品
        # 验证是否有用户的历史记录
        if user_id in self.trainSet:
            pass
        else:
            print("use other method to recommend !")
        try:
            watched_movies = self.trainSet[user_id]
        except KeyError:
            print(user_id + " is not exits")

        for movie, rating in watched_movies.items():
            # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
            for related_movie, w in \
                    sorted(self.movie_sim_matrix[movie].items(),
                           key=itemgetter(1), reverse=True)[:K]:
                # 若该物品为当前物品，跳过
                if related_movie in watched_movies:
                    continue
                # 计算用户user对related_movie的偏好值，初始化该值为0
                self.rank.setdefault(related_movie, 0)
                # 通过与其相似物品对物品related_movie的偏好值相乘并相加。
                # 排名的依据—— > 推荐电影与该已看电影的相似度(累计) * 用户对已看电影的评分
                self.rank[related_movie] += w * float(rating)
        return sorted(self.rank.items(), key=itemgetter(1), reverse=True)[:N]

    # 产生推荐并通过准确率、召回率和覆盖率进行评估
    def evaluate(self):
        print('算法评价过程......')
        N = self.n_rec_movie
        # 准确率和召回率
        # 总命中数
        all_hit = 0
        # 总推荐数
        rec_count = 0
        # 总结果数
        test_count = 0
        # 每个用户的 评价
        # 覆盖率
        all_rec_movies = set()
        # i, user：user_id
        for i, user in enumerate(self.trainSet):
            hit = 0
            # 读取测试集
            test_moives = self.testSet.get(user, {})
            # 推荐集合
            rec_movies = self.recommend(user)
            user_evaluate = {}
            user_evaluate.setdefault('train_len', len(self.trainSet.get(user)))
            user_evaluate.setdefault('test_len', len(test_moives))
            user_evaluate.setdefault('rec_len', len(rec_movies))

            for movie, w in rec_movies:
                if movie in test_moives:
                    # 推荐结果命中
                    hit += 1
                # 所有推荐的电影
                all_rec_movies.add(movie)
            user_evaluate.setdefault('hit', hit)
            all_hit += hit
            rec_count += N

            # 每个用户的 f1 score
            if len(rec_movies) == 0:
                user_precision = 0
            else:
                user_precision = hit / len(rec_movies)
            if len(test_moives) == 0:
                user_recall = 0
            else:
                user_recall = hit / len(test_moives)
            if user_recall + user_precision == 0:
                f1_score = 'error'
            else:
                f1_score = 2 * user_precision * user_recall \
                           / (user_precision + user_recall)
            user_evaluate.setdefault('precision', user_precision)
            user_evaluate.setdefault('recall', user_recall)
            user_evaluate.setdefault('f1_score', f1_score)
            self.evaluates.setdefault(user, user_evaluate)

            test_count += len(test_moives)

        precision = hit / (1.0 * rec_count)
        recall = hit / (1.0 * test_count)
        coverage = len(all_rec_movies) / (1.0 * len(self.movie_popular))
        print('命中=%.4f\t推荐总数=%.4f\t结果集总数=%.4f' % (
            all_hit, rec_count, test_count))
        print('总命中率=%.10f\t总召回率=%.10f\t推荐电影占比=%.10f' % (
            precision, recall, coverage))



if __name__ == "__main__":
    item = ItemCF()
    path = '.\\bigdata\\ratings.csv'
    print(os.path.abspath('.'))
    print(os.path.exists(path))    

    # read_file
    item.get_dataset(path)

    a = datetime.now()
    item.count_user()
    item.users_to_list()
    b = datetime.now()
    item.evaluates.setdefault("method_calc_movie_sim_1", (b - a).seconds)

    a = datetime.now()
    item.calc_movie_sim_cosine()
    b = datetime.now()
    print("clac movie_sim_matrix ", (b - a).seconds)
    item.evaluates.setdefault("method_evaluate", (b - a).seconds)

    ii = 0

    # with open('itemcv_1_1.csv', 'a') as rf:
    #     for i, score in item.evaluates.items():
    #         if ii == 0:
    #             for key in score.keys():
    #                 rf.write(',%s'%key)
    #             ii += 1
    #             rf.write('\n')
    #         rf.write('%s'%i)
    #         for value in score.values():
    #             rf.write(',%s'%value)
    #         rf.write('\n')
    with closing(shelve.open('cosine.data','c')) as sh:
        sh['cosine'] = item.movie_sim_matrix
