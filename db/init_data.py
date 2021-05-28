import pymongo

mongo_ip = "192.168.43.184"
mongo_port = 27017
mongo_user = 'root'
mongo_pwd = 'root'
uri = "mongodb://{0}:{1}@{2}:{3}".format(mongo_user, mongo_pwd,
                                         mongo_ip, mongo_port)

uri = "mongodb://root:root@192.168.43.184:27017"
# train_handler = pymongo.MongoClient().chapter_4.trainSet
# handler = pymongo.MongoClient(uri).chapter_4.ratings
database = pymongo.MongoClient(uri).chapter_4


def load_file(filename):
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


# 初始化 训练数据
def init_ratings(filename, pivot=0.75):
    ratingLen = []
    # 加载文件， 按行读取
    for line in load_file(filename):
        # 读取列属性
        user, movie, rating, timestamp = line.split(',')
        user = int(user)
        movie = int(movie)
        rating = float(rating)
        ratingLen.append({'user': user, 'movie': movie, 'rating': rating})
    database.ratings.insert_many(ratingLen)


# 初始化电影 数据
def init_movie(filename):
    movieLen = []
    # 加载文件， 按行读取
    for line in load_file(filename):
        try:
            movieId, title, genres = line.split(',')
            movieId = int(movieId)
        except ValueError:
            continue
        movieLen.append({'movieId': movieId, 'title': title, 'genres': genres})
    database.movies.insert_many(movieLen)


# 初始化 电影links 数据
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


# 初始化用户表
def init_user(filename):
    # users = set()
    # 加载文件， 按行读取
    data = []
    for line in load_file(filename):
        # 读取列属性
        print(line)
        pwd = '1234'
        user, name, username, _, _ = line.split(',')
        try:
            user = int(user)
        except BaseException:
            pass
        # users.add(user)
        name = name.lower()
        username.lower()
        pwd.lower()
        data.append({
            'userId': user,
            'name': name,
            'username': username,
            'pwd': pwd,
        })
    # set 去重转成字典
    # print(data)
    # print(len(data))
    database.user_detail.insert_many(data)


if __name__ == '__main__':
    # print(load_head('ratings.csv'))
    # print(load_head('movies.csv').split(','))
    #
    # init_user('ratings.csv')
    # print(list(zip([1,2],[3,4])))
    # init_movie('movies.csv')
    # init_ratings('ratings.csv')
    # init_link('links.csv')
    init_user('user_detail.csv')
    # k = 0
    # with open('user_detail.csv') as f:
    #     line = f.readline()
    #     print(line.split(','))
    #     print(f.readline().split(','))
    # for i in load_file('movies.csv'):
    #     print(i.strip(','))
    #     if k > 5:
    #         break
    #     k += 1

    # a = database.movies.find_one({'movieId': 180})
    # b = database.links.find_one({'movieId': 180})
    # a.update(b)
    # print(a)

    # user_rec_cache = database.user_rec_cache


data = \
        {1:
             [{'movieId': 2115,
               'title': 'Indiana Jones and the Temple of Doom (1984)',
               'genres': 'Action|Adventure|Fantasy',
               'imdbId': 'http://www.imdb.com/title/tt87469',
               'tmdbId': 'https://www.themoviedb.org/movie/87',
               'ratings': 76.45141047797219},
              {'movieId': 1196,
               'title': 'Star Wars: Episode V - The Empire Strikes Back (1980)',
               'genres': 'Action|Adventure|Sci-Fi',
               'imdbId': 'http://www.imdb.com/title/tt80684',
               'tmdbId': 'https://www.themoviedb.org/movie/1891',
               'ratings': 53.172590388030244},
              {'movieId': 1923,
               'title': "There's Something About Mary (1998)",
               'genres': 'Comedy|Romance',
               'imdbId': 'http://www.imdb.com/title/tt129387',
               'tmdbId': 'https://www.themoviedb.org/movie/544',
               'ratings': 36.032801193125835},
              {'movieId': 1200,
               'title': 'Aliens (1986)',
               'genres': 'Action|Adventure|Horror|Sci-Fi',
               'imdbId': 'http://www.imdb.com/title/tt90605',
               'tmdbId': 'https://www.themoviedb.org/movie/679',
               'ratings': 35.64895451997378},
              {'movieId': 480,
               'title': 'Jurassic Park (1993)',
               'genres': 'Action|Adventure|Sci-Fi|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt107290',
               'tmdbId': 'https://www.themoviedb.org/movie/329',
               'ratings': 34.97835205157789},
              {'movieId': 1380,
               'title': 'Grease (1978)',
               'genres': 'Comedy|Musical|Romance',
               'imdbId': 'http://www.imdb.com/title/tt77631',
               'tmdbId': 'https://www.themoviedb.org/movie/621',
               'ratings': 30.092855674772846},
              {'movieId': 2028,
               'title': 'Saving Private Ryan (1998)',
               'genres': 'Action|Drama|War',
               'imdbId': 'http://www.imdb.com/title/tt120815',
               'tmdbId': 'https://www.themoviedb.org/movie/857',
               'ratings': 30.014776987975168},
              {'movieId': 1036,
               'title': 'Die Hard (1988)',
               'genres': 'Action|Crime|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt95016',
               'tmdbId': 'https://www.themoviedb.org/movie/562',
               'ratings': 29.529508499632268},
              {'movieId': 47,
               'title': 'Seven (a.k.a. Se7en) (1995)',
               'genres': 'Mystery|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt114369',
               'tmdbId': 'https://www.themoviedb.org/movie/807',
               'ratings': 29.282623651730994},
              {'movieId': 2683,
               'title': 'Austin Powers: The Spy Who Shagged Me (1999)',
               'genres': 'Action|Adventure|Comedy',
               'imdbId': 'http://www.imdb.com/title/tt145660',
               'tmdbId': 'https://www.themoviedb.org/movie/817',
               'ratings': 25.84264861921086}
              ]
         }
