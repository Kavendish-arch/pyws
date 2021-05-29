from db.init_data import database
from logging import Logger


def user_record(user_id):
    """
    获取播放记录 用户端
    :return: 播放记录
    """
    base_data = database.ratings.find({
        'user': user_id
    })
    extent_data = []
    for i in base_data:
        tmp = i.copy()
        movie = database.movies.find_one({
            'movieId': i.get('movie')
        }, {
            '_id': 0
        })
        user = database.user_detail.find_one({
            'userId': i.get('user')
        }, {
            '_id': 0,
            'username': 1
        })
        tmp['movie'] = movie
        tmp['user'] = user.get('username')

        extent_data.append(tmp)
    return extent_data


def movie_record():
    pass


def movie_detail():
    """
    电影信息管理
    :return:
    """
    # 电影播放次数 {{ "movieId':total }}
    movie_total = {}
    # 电影的链接管理{
    #   {
    #   'movieId': 1,
    #   'imdbId': 'http://www.imdb.com/title/tt114709',
    #   'tmdbId': 'https://www.themoviedb.org/movie/862'
    #   }
    # }
    movie_link = {}

    # 最后展示的电影记录
    movie_details_record = []

    for data in database.ratings.find({}):
        movie_total.setdefault(data.get('movie'), 0)
        movie_total[data.get('movie')] += 1


    for i in database.links.find({

    }, {
        '_id': 0
    }):
        movie_link.setdefault(i.get('movieId'), i)

    for item in database.movies.find({

    },{
        '_id': 0
    }).skip(0).limit(20):
        # 加入 movie total message
        item.setdefault('movie_total', 0)
        item['movie_total'] = movie_total.get(item.get('movieId', 0))
        # 加入 Link message
        item.setdefault('movie_link', None)
        item['movie_link'] = movie_link.get(1)

        movie_details_record.append(item)

    return movie_details_record


def update_user(user_id, new_user):
    """
    修改用户信息的方法
    :param user_id:
    :param new_user:
    :return:
    """
    base_user = database.user_detail.find_one({
        'userId': user_id
    })
    base_user.update(new_user)
    if database.user_detail.replace_one(base_user, new_user):
        return True
    else:
        return False


def get_user_detail():
    """
    获取用户信息
    :return:
    """
    base_user = database.user_detail.find({

    },{
        'pwd': 0,
    }).skip(0).limit(10)

    base_user_list = []
    for i in base_user:
        base_user_list.append(i)

    return base_user_list


if __name__ == "__main__":
    data = user_record(1)

    # data = movie_detail()
    # data = get_user_detail()

    print(type(data))
    for i in data:
        print(i)
        # break
