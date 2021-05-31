import redis

host_ip = "192.168.43.184"
redis_name = 'root'
redis_pwd = 1234

client = redis.Redis(host=host_ip, username=redis_name, password=redis_pwd)


class RedisUtil(object):
    def __init__(self, client):
        self.client = client


    def set_token(self, username, userId):
        pass