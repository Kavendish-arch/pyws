from db.init_data import database
from logging import Logger


def user_record(user_id, page=0, count=20):
    # 获取用户的播放记录
    base_data = database.ratings.find({
        'user': user_id
    }).skip(page * count).limit(count)

    # 播放记录拓展，
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


def count_user_table(db, page, count, user):
    total = database[db].find({
        'user': user,
    }).count()

    if total % count == 0:
        max_page_index = total / count
    else:
        max_page_index = int(total / count) + 1

    page_info = {
        'min_page_index': 1,
        'max_page_index': max_page_index,
        'page_id': page,
        'count': count,
    }
    return page_info


def count_table(db, page, count, condition=None):
    if condition:
        total = database[db].find(condition).count()
    else:
        total = database[db].find({}).count()

    if total % count == 0:
        max_page_index = total / count
    else:
        max_page_index = int(total / count) + 1

    page_info = {
        'min_page_index': 1,
        'max_page_index': max_page_index,
        'page_id': page,
        'count': count,
    }
    return page_info


def movie_detail(page, count):
    """
    获取电影信息
    """
    # 电影播放次数 {{ "movieId':total }}
    movie_total = {}
    for data in database.ratings.find({}):
        movie_total.setdefault(data.get('movie'), 0)
        movie_total[data.get('movie')] += 1

    # 电影链接
    movie_link = {}
    # 最后展示的电影记录
    movie_details_record = []
    # 统计电影

    for i in database.link2.find({

    }, {
        '_id': 0
    }):
        movie_link.setdefault(i.get('movieId'), i)

    for item in database.movies.find({

    },
    {
        '_id': 0
    }).skip(page * count).limit(count):

        # 加入 movie total message
        item.setdefault('movie_total', 0)
        item['movie_total'] = movie_total.get(item.get('movieId'))
        # 加入 Link message
        item.setdefault('movie_link', None)
        item['movie_link'] = movie_link.get(item.get('movieId'))
        item['video_url'] = movie_link.get(item.get('movieId')).get('video_url')

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


def get_user_detail(index_page=0, count=10):
    """
    获取用户信息
    :return:
    """
    base_user = database.user_detail.find({

    }, {
        'pwd': 0,
    }).skip(index_page * count).limit(count)

    base_user_list = []
    for i in base_user:
        base_user_list.append(i)

    return base_user_list


if __name__ == "__main__":
    # data = user_record(1)

    data = movie_detail(0, 10)
    # data = get_user_detail(5, 10)

    print(type(data))
    for i in data:
        print(i)
        break

    # print(count_table('ratings', 1, 10, {'user': 1}))
