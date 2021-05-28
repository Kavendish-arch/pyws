from db.init_data import database
from ItemCF.ItemCF_db import ItemBasedCF
from UserCF.UserCF_1 import UserBasedCF
from threading import Thread
import re


def get_movies(user_id):

    movie_handler = database.movies
    link_handler = database.links

    itemCF = ItemBasedCF()
    itemCF.get_dataset()

    userCF = UserBasedCF()
    userCF.init_dataset()

    # 计算相似性
    itemCF.calc_movie_sim()
    userCF.calc_user_sim()

    # 推荐结果
    user_rec_cache_list = []

    t1 = Thread(target=itemCF.recommend, args=(user_id,))
    t2 = Thread(target=userCF.recommend, args=(user_id,))
    # rec_itemCF = itemCF.recommend(user_id)
    # rec_userCF = userCF.recommend(user_id)
    t1.start()
    t2.start()

    rec = itemCF.result_rec + userCF.result_rec
    # print(rec_userCF, rec_itemCF)

    for rank in rec:
        a = movie_handler.find_one({'movieId': rank[0]}, {'_id': 0})
        b = link_handler.find_one({'movieId': rank[0]}, {'_id': 0})
        try:
            a.update(b)
            a.setdefault('ratings', rank[1])
        except AttributeError:
            continue
        user_rec_cache_list.append(a)
    result = {"userId": user_id, 'movies': user_rec_cache_list}

    return result


def get_movies_cache(user_id):
    return database.user_rec_cache.find_one({'userId': user_id}, {'_id': 0})


def search_movies(condition):

    movie_list = database.movies.find({
        '$or': [
            {'title': condition},
            {'genres': condition}
        ]
    },
        {
            '_id': 0
        }
    )
    result = []
    for i in movie_list:
        d = i.copy()
        # print(type(i), i)
        t = database.links.find_one({
            'movieId': i.get('movieId')
        },
            {
                "_id": 0,
                "imdbId": 1,
                "tmdbId": 1,
            }
        )
        try:
            d.update(t)
        except TypeError:
            continue
        except BaseException:
            continue
        result.append(d)
    return result


def search_movies_extention(title, genre):

    movie_list = database.movies.find({
        '$and': [
            {'title': title},
            {'genres': genre}
        ]
    },
        {
            '_id': 0
        }
    )
    result = []
    for i in movie_list:
        d = i.copy()
        # print(type(i), i)
        t = database.links.find_one({
            'movieId': i.get('movieId')
        },
            {
                "_id": 0,
                "imdbId": 1,
                "tmdbId": 1,
            }
        )
        try:
            d.update(t)
        except TypeError:
            continue
        except BaseException:
            continue
        result.append(d)
    return result


def valid_logined(user_name, user_pwd):
    user_detail = database.user_detail.find_one({
        'username':user_name,
        'pwd':user_pwd
    },
        {
            '_id': 0,

        }
    )
    print(user_detail)
    if user_detail:
        return {
            'username': user_detail.get('username'),
            'login_user': str(user_detail.get("name")),
            'login_status': 'True',
            'login_role': 'admin',
            'login_id': str(user_detail.get('userId')),
        }
    else:
        return False


def valid_sign(user_dict):
    return True
    user_detail = database.user_detail.find_one({
        'username': "",
        'pwd': "",
    },
        {
            '_id': 0,

        }
    )
    print(user_detail)
    if user_detail:
        return {
            'username': user_detail.get('username'),
            'login_user': str(user_detail.get("name")),
            'login_status': 'True',
            'login_role': 'admin',
            'login_id': str(user_detail.get('userId')),
        }
    else:
        return False


def is_login(req, sess):
    user_name = req.cookies.get('login_user')
    status = req.cookies.get('login_status')
    role = req.cookies.get('login_role')
    user_id = req.cookies.get('login_id')
    if "username" in sess:
        if user_name and status and role and user_id:
            return True
        else:
            return False
    else:
        return False


if __name__ == "__main__":
    '''
    data = database.user_id.find({}, {'_id': 0})
    j = []
    for i in data:
        j.append(i.get('userId'))
    # print(len(list(data)))
    users = j
    for user in users:
        if user < 78:
            continue
        try:
            pass
            # data = get_movies(user)
            # database.user_rec_cache.insert_one(data).inserted_id
        except BaseException:
            continue

    print(get_movies_cache(4))
    user_one = database.user_detail.find_one({})
    print(database.user_detail.find_one({}))
    # for k,v in user_one.items():
    #     print(type(k), "k", type(v), "v")
    print(valid_logined('Braund', '1234'))
    '''
    title = ".*{0}.*{1}.*".format("", "2017")
    genre = ".*{0}.*{1}.*".format("Action", "")
    data = search_movies_extention(re.compile(title), genre=genre)
    for i in data:
        print(i)
    print(type(data), len(data))
