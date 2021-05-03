import shelve
from contextlib import closing

with closing(shelve.open('tmp_jacard_2.data', 'c')) as sh:
    evaluates = sh['evaluates']
    key_list = evaluates.keys()

    print("all_hit", evaluates)
