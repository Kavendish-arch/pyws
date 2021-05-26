from db.init_data import database
from ItemCF.ItemCF_db import ItemBasedCF


def get_movies(user_id):

    movie_handler = database.movies
    link_handler = database.links

    itemCF = ItemBasedCF()
    itemCF.get_dataset()

    # 计算相似性
    itemCF.calc_movie_sim()
    user_rec_cache_list = []

    rec = itemCF.recommend(user_id)
    tmp = {}
    for i in rec:
        tmp.setdefault(i[0], i[1])

    print(tmp)


    for i in rec:
        a = movie_handler.find_one({'movieId': i[0]}, {'_id': 0})
        b = link_handler.find_one({'movieId': i[0]}, {'_id': 0})
        try:
            a.update(b)
            a.setdefault('ratings', i[1])
        except AttributeError:
            continue
        user_rec_cache_list.append(a)
    result = { user_id: user_rec_cache_list }

    return result


if __name__ == "__main__":

    data = get_movies(2)

    print(data)
