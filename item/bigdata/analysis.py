import shelve
import os
from contextlib import closing
import numpy as np

precision, recall, f1_score = \
    np.loadtxt('data.csv', delimiter=',',
               usecols=(5, 6, 7), unpack=True)
pre = np.where(precision > 0)
rec = np.where(recall > 0)
f1 = np.where(f1_score > 0)
a = precision[pre]
b = recall[rec]
c = f1_score[f1]


def ping_jia(*a, **k):
    """
    :param a:
    :param k:
    :return: 平均数，长度，最大值，最小值，中位数
    """
    result = []
    for i in a:
        result.append(
            {
                "mean": np.mean(i),
                "len": len(i),
                "max = ": np.max(i),
                "min": np.min(i),
                "median": np.median(i),
            }
        )
        # print("mean = ",np.mean(i), "len = ",len(i))
        # print("max = ",np.max(i), "\nmin = ",
        # np.min(i), "\nmedian = ", np.median(i))
        # print()
    # print(k)
    return result


print(ping_jia(a, b, c))

# ['evaluates', 'method_calc_movie_sim_2','method_evaluate']
with closing(shelve.open('itemCV_2_3.data', 'c')) as sh:
    # evaluates = sh['evaluates']
    # key_list = evaluates.keys()
    # print(key_list)
    #
    # print("all_hit", evaluates)
    data = {}
    for i in sh.keys():
        data.setdefault(i, sh.get(i))

    # print(data.get("method_evaluate"))
print("userCF_1_1.data")
with closing(shelve.open('userCF_1_1.data', 'r')) as sh:
    ii = 0
    for i in sh.keys():
        ii += 1;
        if ii <= 610:
            continue
        print(sh.get(i))

# from util import tool
# tool.save_as_csv(userCF, "userCF_1_1.csv")
print(os.path.dirname('.'))
