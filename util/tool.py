import random
import shelve
from contextlib import closing
from operator import itemgetter


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


# 保存为csv
def save_as_csv(item, f_name):
    ii = 0
    with open(f_name, 'a') as rf:
        for i, score in item.evaluates.items():
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
    with closing(shelve.open(f_name, 'c')) as sh:
        for i in keys:
            sh[i] = item.get(i)


if __name__ == "__main__":
    path = '..\\file\\ratings.csv'
    trainSet, testSet = get_dataset(path)
