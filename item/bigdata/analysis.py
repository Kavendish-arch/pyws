import shelve
import os
from contextlib import closing

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
