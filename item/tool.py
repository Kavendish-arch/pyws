import os
import random
import csv
# yield 加载文件


def load_file(filename):
    """open file load data"""
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


def random_list(len_l, max_limit, func):
    data_r = []
    for _ in range(len_l):
        data_r.append(func(max_limit))
    return data_r


def random_num(max_limit):
    return random.random() * max_limit


def random_int(max_limit):
    return round(random.random() * max_limit)


if __name__ == "__main__":
    path = os.path.abspath(os.curdir) + \
           "\\bigdata\\ml-latest-small\\movies.csv"

    data = {}
    for line in load_file(path):
        movie_id, title = line[0], line[1:]
        data.setdefault(movie_id, title)
    print(data)