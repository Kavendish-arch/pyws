from db.init_data import database, tmp_data
from ItemCF.ItemCF_db import ItemBasedCF
from UserCF.UserCF_1 import UserBasedCF
from threading import Thread
import re
from config import get_md5
from db.redisUtil import client
from datetime import datetime


def init_movies_sim():
    """
    推荐信息
    """
    itemCF = ItemBasedCF()
    itemCF.get_dataset()

    userCF = UserBasedCF()
    userCF.init_dataset()

    # 计算相似性
    itemCF.calc_movie_sim()
    database.movie_sim_cache.insert_many(itemCF.movie_sim_matrix)

    userCF.calc_user_sim()

    database.user_sim_cache.insert_many(userCF.user_sim_matrix)


def get_movies(user_id):
    """
    推荐信息
    :param user_id:
    :return:
    """
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
    database.user_rec_cache.update({
        'userId': user_id,
    },
    {
        '$set': {
            'movies': user_rec_cache_list
        }
    })
    return result


def get_movies_cache(user_id):
    """从缓存中获取推荐信息"""
    result = database.user_rec_cache.find_one({'userId': user_id}, {'_id': 0})
    if result:
        return result
    else:
        return None


def search_movies(condition, page, count):

    movie_list = database.movies.find({
        '$or': [
            {'title': condition},
            {'genres': condition}
        ]
    },
        {
            '_id': 0
        }
    ).skip(page * count).limit(count)

    return movie_extent(movie_list)


def movie_extent(movie_list):
    result = []
    for i in movie_list:
        # print(i)
        d = i.copy()
        t = database.link2.find_one({
            'movieId': i.get('movieId')
        },
            {
                "_id": 0,
                "imdbId": 1,
                "tmdbId": 1,
                'img_url': 1,
            }
        )
        try:
            d.update(t)
        except TypeError:
            continue
        except BaseException:
            continue
        result.append(d)
    # database.movies_cache.insert_many(result)
    return result


def search_movies_extention(title, genre, year):

    movie_list = database.movies.find({
        '$and': [
            {'title': title},
            {'genres': genre},
            {'title': year}
        ]
    },
        {
            '_id': 0
        }
    ).limit(20)

    return movie_extent(movie_list)


def valid_name(user_name):
    user_detail = database.user_detail.find_one({
        'username':user_name
    })

    return user_detail


def valid_logout(token):
    client.expire(token, 6)




def valid_logined(user_name, user_pwd):
    user_detail = database.user_detail.find_one({
        'username': user_name,
        'pwd': user_pwd
    },
        {
            '_id': 0,

        }
    )
    md5_pwd = get_md5(user_detail.get('username'), user_detail.get('pwd'))
    client.set(md5_pwd, md5_pwd)
    print(md5_pwd)
    # 设置token 过期时间
    client.expire(md5_pwd, 60 * 60 * 2)
    # print(user_detail)


    if user_detail:
        return {
            'username': user_detail.get('username'),
            'login_user': str(user_detail.get("name")),
            'login_status': 'True',
            'login_role': 'admin',
            'login_id': str(user_detail.get('userId')),
            'token_pwd': str(md5_pwd)
        }
    else:
        return False





def valid_sign(user_dict):
    username = user_dict.get('username', None)
    pwd = user_dict.get('password', None)
    pass


def valid_change_pwd(user_dict, new_dict):
    # 修改用户密码的代码
    if 'password' not in new_dict:
        return False
    new_dict['pwd'] = new_dict.pop('password')
    # 验证存在，
    username = user_dict.get('username', None)

    if username is None:
        return False

    user_detail = database.user_detail.find_one({
        'username': username,
    },
        {
            '_id': 0,
        }
    )
    if user_detail is None:
        return False

    user_detail.update(new_dict)

    print(user_detail)
    if user_detail:
        database.user_detail.update_one({
            'username': username
        }, {
            '$set': user_detail
        })
        return True
    else:
        return False


def is_login(req, sess):
    # 登录验证
    try:
        cookie_token = req.cookies.get('token_pwd')
        session_token = sess['token_pwd']
    except BaseException:
        return False

    if session_token is None:
        # 数据库中查询
        if client.exists(cookie_token):
            session_token = client.get(session_token)
    if cookie_token == session_token and cookie_token is not None:
        # print("token 验证通过")
        return True

    return False




if __name__ == "__main__":

    condition = re.compile(".*Com.*")
    # data = search_movies(condition)
    data = database.movies.find({
        "$or": [
            {'title': condition},
            {'genres': condition}
        ]
    })
    print(data)
    # 查找用户测试

    '''
    用户具体信息
    user_one = database.user_detail.find_one({})
    print(database.user_detail.find_one({}))
    # for k,v in user_one.items():
    #     print(type(k), "k", type(v), "v")
    print(valid_logined('Braund', '1234'))
    '''

    """
    模糊查找
    title = ".*2017.*"
    data = search_movies(re.compile(title), 0, 20)
    for i in data:
        print(i)

    """
    # 存储相似矩阵
    # init_movies_sim()
