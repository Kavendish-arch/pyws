from pymongo import MongoClient
from db.init_data import handler


def query_info():
    return handler.find()


class DataBaseManager(object):
    def __init__(self):
        pass


if __name__ == "__main__":
    for i in query_info():
        print(i)
