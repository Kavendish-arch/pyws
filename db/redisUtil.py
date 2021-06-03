import redis
from db.init_data import database
host_ip = "192.168.43.184"
host_ip = "192.168.1.115"
redis_name = 'root'
redis_pwd = 1234

client = redis.Redis(host=host_ip, username=redis_name, password=redis_pwd)


class RedisUtil(object):
    def __init__(self):
        self.client = client
        pass

    def set_token(self, username, userId):
        pass

    def is_nick_already_exists(self, username):
        result = database.user_detail.find_one({
            'username': username
        },{
            '_id':0,
            'username':1,
        })
        return result
