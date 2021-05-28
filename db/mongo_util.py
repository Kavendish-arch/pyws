import pymongo
import redis

ip_db = '192.168.0.32'
port_db = 6379
db_pass = '1234'
user = 'admin'
pwd = 'admin'
uri = "mongodb://{0}:{1}@{2}:27017/admin".format(user, pwd, ip_db)


if __name__ == "__main__":
    # client = pymongo.MongoClient(host=ip_db, port=27017)
    client = pymongo.MongoClient(uri)
    dblist = client.list_database_names()
    print("mongodb : ",dblist)
    # r1 = redis.Redis(host=ip_db, port=port_db, password=db_pass)
    # print(r1)
    # print(r1.get('key'), type(r1.get('key')))

    # d = {'1':1}
    # r1.hmset('1',d)
    # print(r1.hgetall('1'), type(r1.hgetall('1')))
