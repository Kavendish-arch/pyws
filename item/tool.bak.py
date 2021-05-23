import os
import random
import csv
import numpy as np
# yield 加载文件


def load_file(filename):
    """open file load data 使用了csv 模块"""
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


def random_list(len_l, max_limit, func):
    data_r = []
    for _ in range(len_l):
        data_r.append(func(max_limit))
    return data_r


def random_num(max_limit):
    return random.random() * max_limit


def random_int(max_limit):
    return round(random.random() * max_limit)


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


def jacard(movie_popular, movie_sim_matrix):
    print("Calculating movie similarity matrix ...")
    for m1, related_movies in movie_sim_matrix.items():
        for m2, count in related_movies.items():
            # 注意0向量的处理，即某电影的用户数为0
            if movie_popular[m1] == 0 or movie_popular[m2] == 0:
                movie_sim_matrix[m1][m2] = 0
            else:
                movie_sim_matrix[m1][m2] = count / (movie_popular[m1] +
                                                    movie_popular[m2] - count)
    print('Calculate movie similarity matrix success!')
    return movie_sim_matrix

    


# 统计电影的播放次数，movie_movie 矩阵
def count_movie(trainSet):
    movie_popular = {}
    for user, movies in trainSet.items():
        for movie in movies:
            if movie not in movie_popular:
                movie_popular[movie] = 0
            movie_popular[movie] += 1
    return movie_popular


# 建立同现矩阵
def build_movie_matrix(trainSet):
    # 统计电影被看的次数
    movie_popular = count_movie(trainSet)
    # movie_count = len(movie_popular)
    # print("Total movie number = %d" % movie_count)

    # 建立 movie and movie 矩阵
    movie_sim_matrix = {}
    # 遍历训练数据，获得用户对有过的行为的物品
    for user, movies in trainSet.items():
        # 遍历该用户每件物品项
        for m1 in movies:
            # 遍历该用户每件物品项
            for m2 in movies:
                # 若该项为当前物品，跳过
                if m1 == m2:
                    continue
                movie_sim_matrix.setdefault(m1, {})
                movie_sim_matrix[m1].setdefault(m2, 0)
                # 同一个用户，遍历到其他用品则加1
                movie_sim_matrix[m1][m2] += 1
    # print("Build 同现矩阵co-rated users matrix success!")
    return movie_popular, movie_sim_matrix


# 针对目标用户U，找到K部相似的电影，并推荐其N部电影，
# 用户未产生过行为的物品
def recommend(aim, user_id):
    # 推荐的数量
    K = aim.n_sim_movie
    N = aim.n_rec_movie
    # 用户(user_id)对物品的偏好值序列，生成推荐列表
    aim.rank = {}
    # 用户user产生过行为的物品，与物品item按相似度从大到小排列，取与物品item相似度最大的k个商品
    # 验证是否有用户的历史记录
    try:
        watched_movies = aim.trainSet[user_id]
    except KeyError:
        print(user_id + " is not exits")

    for movie, rating in watched_movies.items():
        # 遍历与物品item最相似的前k个产品，获得这些物品及相似分数
        for related_movie, w in \
                sorted(aim.movie_sim_matrix[movie].items(),
                       key=itemgetter(1), reverse=True)[:K]:
            # 若该物品为当前物品，跳过
            if related_movie in watched_movies:
                continue
            # 计算用户user对related_movie的偏好值，初始化该值为0
            aim.rank.setdefault(related_movie, 0)
            # 通过与其相似物品对物品related_movie的偏好值相乘并相加。
            # 排名的依据—— > 推荐电影与该已看电影的相似度(累计) * 用户对已看电影的评分
            aim.rank[related_movie] += w * float(rating)
    return sorted(aim.rank.items(), key=itemgetter(1), reverse=True)[:N]


# 产生推荐并通过准确率、召回率和覆盖率进行评估
def evaluate(aim):
    print('算法评价过程......')
    N = aim.n_rec_movie
    # 准确率和召回率
    # all_hit 总命中数, rec_count 总推荐数 test_count 总正确数
    all_hit = 0
    rec_count = 0
    test_count = 0
    # 推荐的所有电影集合，算法推荐结果覆盖率
    all_rec_movies = set()

    # i, user：user_id
    for i, user in enumerate(aim.trainSet):
        # hit 用户命中率
        hit = 0
        user_evaluate = {}

        # 读取测试集
        test_movies = aim.testSet.get(user, {})
        # 推荐集合
        rec_movies = recommend(aim, user)

        # 数据记录环节
        user_evaluate.setdefault('train_len', len(aim.trainSet.get(user)))
        user_evaluate.setdefault('test_len', len(test_movies))
        user_evaluate.setdefault('rec_len', len(rec_movies))

        for movie, w in rec_movies:
            if movie in test_movies:
                # 推荐结果命中
                hit += 1
            # 所有推荐的电影
            all_rec_movies.add(movie)

        # 记录
        user_evaluate.setdefault('hit', hit)
        all_hit += hit
        rec_count += N

        x = len(rec_movies)
        y = len(test_movies)
        # 每个用户的 f1 score
        user_precision = 0 if x == 0 else hit / x
        user_recall = 0 if y == 0 else hit / y

        if user_recall + user_precision == 0:
            f1_score = -1
        else:
            f1_score = 2 * user_precision * user_recall \
                       / (user_precision + user_recall)
        user_evaluate.setdefault('precision', user_precision)
        user_evaluate.setdefault('recall', user_recall)
        user_evaluate.setdefault('f1_score', f1_score)
        # 存入集合
        aim.evaluates.setdefault(user, user_evaluate)

        test_count += len(test_movies)

    precision = all_hit / (1.0 * rec_count)
    recall = all_hit / (1.0 * test_count)
    coverage = len(all_rec_movies) / (1.0 * len(aim.movie_popular))

    aim.evaluates.setdefault('all_hit', all_hit)
    aim.evaluates.setdefault('rec_count', rec_count)
    aim.evaluates.setdefault('res_count', test_count)
    aim.evaluates.setdefault('precision', precision)
    aim.evaluates.setdefault('recall', recall)
    aim.evaluates.setdefault('coverage', coverage)

