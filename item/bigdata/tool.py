
import random

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
    # 统计电影被看的次数
    movie_popular = {}
    for user, movies in trainSet.items():
        for movie in movies:
            if movie not in movie_popular:
                movie_popular[movie] = 0
            movie_popular[movie] += 1
    movie_count = len(movie_popular)
    print("Total movie number = %d" % movie_count)

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
    print("Build 同现矩阵co-rated users matrix success!")
    return movie_popular, movie_sim_matrix

    