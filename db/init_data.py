import pymongo
import random
import datetime

uri = "mongodb://root:root@192.168.43.184:27017"
train_handler = pymongo.MongoClient().chapter_4.trainSet
handler = pymongo.MongoClient(uri).chapter_4.ratings
test_handler = pymongo.MongoClient().chapter_4.testSet
database = pymongo.MongoClient(uri).chapter_4


def load_file(filename):
    head = {}
    with open(filename, 'r', encoding='utf-8') as f:
        for i, line in enumerate(f):
            if i == 0:
                # 去掉文件第一行的title
                head = line.strip('\r\n')
                print(head)
                continue
            yield line.strip('\r\n')
    print('Load %s success!' % filename)


def load_head(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        line = f.readline()
        return line.strip('\r\n')


# 读文件得到“用户-电影”数据
def init_ratings(filename, pivot=0.75):
    ratingLen = []
    rating_len = 0
    head = load_head(filename)
    lambda x,y:zip(x,y)
    # 加载文件， 按行读取
    for line in load_file(filename):
        # 读取列属性
        user, movie, rating, timestamp = line.split(',')
        user = int(user)
        movie = int(movie)
        rating = float(rating)
        # 数据划分测试集合和数据集合 (0,1) < (0,pivot)
        ratingLen.append({'user': user, 'movie': movie, 'rating': rating})
    handler.insert_many(ratingLen)


def init_movie(filename):
    movieLen = []
    rating_len = 0
    # 加载文件， 按行读取
    for line in load_file(filename):
        # 读取列属性

        try:
            movieId, title, genres = line.split(',')
            movieId = int(movieId)
        except ValueError:
            # print(line)
            continue
        # 数据划分测试集合和数据集合 (0,1) < (0,pivot)
        movieLen.append({'movieId': movieId, 'title': title, 'genres': genres})
    database.movies.insert_many(movieLen)


def init_link(filename):
    link_list = []
    for line in load_file(filename):
        movieId, imdbId, tmdbId = line.split(',')
        try:
            movieId, imdbId, tmdbId = int(movieId), int(imdbId), int(tmdbId)
        except ValueError:
            print(line)
        link_list.append({
            'movieId': movieId,
            'imdbId': imdbId,
            'tmdbId': tmdbId,
        })
    database.links.insert_many(link_list)


if __name__ == '__main__':
    print(load_head('ratings.csv'))
    print(load_head('movies.csv').split(','))
    # print(list(zip([1,2],[3,4])))
    # init_movie('movies.csv')
    # init_ratings('ratings.csv')
    # init_link('links.csv')
    k = 0
    # for i in load_file('movies.csv'):
    #     print(i.strip(','))
    #     if k > 5:
    #         break
    #     k += 1

    a = database.movies.find_one({'movieId': 180})
    b = database.links.find_one({'movieId': 180})
    a.update(b)
    print(a)

    user_rec_cache = database.user_rec_cache

