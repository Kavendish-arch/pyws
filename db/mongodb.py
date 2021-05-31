# 要添加一个新单元，输入 '# %%'
# 要添加一个新的标记单元，输入 '# %% [markdown]'
# %%
from IPython import get_ipython

# %%
txt = '''
    <link type="text/css" rel="stylesheet" href="css/chocolat.css"
          media="screen"/>
    <link type="text/css" rel="stylesheet" href="css/popuo-box.css"
          media="all"/>

    <!--local CSS-->
    <link type="text/css" rel="stylesheet" href="css/style.css" media="all"/>

    <!--JS-->
    <script type="text/javascript" src="{{ url_for('static',"js/jquery-1.11.1.min.js") }}"></script>
    <script type="text/javascript" src="{{ url_for('static',"js/easing.js") }}"></script>
    <script type="text/javascript" src="{{ url_for('static',"js/move-top.js") }}"></script>
    <script type="text/javascript" src="{{ url_for('static',"js/wow.min.js") }}"></script>
'''
import re 
m = r'src=".*"'
prog = re.compile(m)
result = re.findall(prog, txt)
result
for i in result:
    print("{{ url_for('static',%s) }}" % i.split('=')[1])
    # print(i.split('=')[1])
    


# %%
user_rec_cache = [{'movieId': 2115, 'title': 'Indiana Jones and the Temple of Doom (1984)', 'genres': 'Action|Adventure|Fantasy', 'imdbId': 87469, 'tmdbId': 87, 'ratings': 76.45141047797219}, {'movieId': 1196, 'title': 'Star Wars: Episode V - The Empire Strikes Back (1980)', 'genres': 'Action|Adventure|Sci-Fi', 'imdbId': 80684, 'tmdbId': 1891, 'ratings': 53.172590388030244}, {'movieId': 1923, 'title': "There's Something About Mary (1998)", 'genres': 'Comedy|Romance', 'imdbId': 129387, 'tmdbId': 544, 'ratings': 36.032801193125835}, {'movieId': 1200, 'title': 'Aliens (1986)', 'genres': 'Action|Adventure|Horror|Sci-Fi', 'imdbId': 90605, 'tmdbId': 679, 'ratings': 35.64895451997378}, {'movieId': 480, 'title': 'Jurassic Park (1993)', 'genres': 'Action|Adventure|Sci-Fi|Thriller', 'imdbId': 107290, 'tmdbId': 329, 'ratings': 34.97835205157789}, {'movieId': 1380, 'title': 'Grease (1978)', 'genres': 'Comedy|Musical|Romance', 'imdbId': 77631, 'tmdbId': 621, 'ratings': 30.092855674772846}, {'movieId': 2028, 'title': 'Saving Private Ryan (1998)', 'genres': 'Action|Drama|War', 'imdbId': 120815, 'tmdbId': 857, 'ratings': 30.014776987975168}, {'movieId': 1036, 'title': 'Die Hard (1988)', 'genres': 'Action|Crime|Thriller', 'imdbId': 95016, 'tmdbId': 562, 'ratings': 29.529508499632268}, {'movieId': 47, 'title': 'Seven (a.k.a. Se7en) (1995)', 'genres': 'Mystery|Thriller', 'imdbId': 114369, 'tmdbId': 807, 'ratings': 29.282623651730994}, {'movieId': 2683, 'title': 'Austin Powers: The Spy Who Shagged Me (1999)', 'genres': 'Action|Adventure|Comedy', 'imdbId': 145660, 'tmdbId': 817, 'ratings': 25.84264861921086}]
tmp = {2115: 76.45141047797219, 1196: 53.172590388030244, 1923: 36.032801193125835, 1200: 35.64895451997378, 480: 34.97835205157789, 1380: 30.092855674772846, 2028: 30.014776987975168, 1036: 29.529508499632268, 47: 29.282623651730994, 2683: 25.84264861921086}


# %%
get_ipython().system('pip install pymongo')


# %%
import pymongo
uri = 'mongodb://root:root@192.168.43.184:27017'
database = pymongo.MongoClient(uri).chapter_4
handler = database.user_rec_cache
print(handler)


# %%
# handler.insert_one({2:[1,2,3,4]})
# # {2:user_rec_cache}


# %%
a = database.movies.find({})
for i in a:
    print(i)
print("OK")


# %%
user_rec_cache_dict = {}
for i in user_rec_cache:
    user_rec_cache_dict.setdefault(i.get('movieId'), i)
user_rec_cache_dict
{2:user_rec_cache}


# %%
imdbId is an identifier for movies used by <http://www.imdb.com>. E.g., the movie Toy Story has the link <http://www.imdb.com/title/tt0114709/>.

tmdbId is an identifier for movies used by <https://www.themoviedb.org>. E.g., the movie Toy Story has the link <https://www.themoviedb.org/movie/862>.


# %%
for i in user_rec_cache:
    i['tmdbId'] = "https://www.themoviedb.org/movie/%d" % i.get('tmdbId')
    i['imdbId'] = "http://www.imdb.com/title/tt%d" % i.get('imdbId')
user_rec_cache


# %%
import _thread
import time

# 为线程定义一个函数
def print_time( threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: 无法启动线程")

while 1:
   pass


# %%
result = [(2959, 3.975187754112997), (2571, 3.1863064439122946), (4993, 3.0730853566355294), (7153, 2.874261116014712), (593, 2.845940435975078), (527, 2.7697221727814845), (356, 2.5542273693194986), (116797, 2.3844371818347643), (44191, 2.3428834133945466), (5952, 2.32666188645332), (2959, 19.175608046298752), (122904, 17.22407608875293), (68954, 16.651849160978664), (72998, 15.875093910893185), (109374, 15.191764817053288), (59315, 14.857106275889432), (69122, 14.38128225841483), (73017, 14.235805245090482), (2571, 14.107013048746147), (7153, 13.991967867580199)]


# %%


result = {2: [{'movieId': 2959, 'title': 'Fight Club (1999)', 'genres': 'Action|Crime|Drama|Thriller', 'imdbId': 137523, 'tmdbId': 550, 'ratings': 19.175608046298752}, {'movieId': 122904, 'title': 'Deadpool (2016)', 'genres': 'Action|Adventure|Comedy|Sci-Fi', 'imdbId': 1431045, 'tmdbId': 293660, 'ratings': 17.22407608875293}, {'movieId': 68954, 'title': 'Up (2009)', 'genres': 'Adventure|Animation|Children|Drama', 'imdbId': 1049413, 'tmdbId': 14160, 'ratings': 16.651849160978664}, {'movieId': 72998, 'title': 'Avatar (2009)', 'genres': 'Action|Adventure|Sci-Fi|IMAX', 'imdbId': 499549, 'tmdbId': 19995, 'ratings': 15.875093910893185}, {'movieId': 59315, 'title': 'Iron Man (2008)', 'genres': 'Action|Adventure|Sci-Fi', 'imdbId': 371746, 'tmdbId': 1726, 'ratings': 14.857106275889432}, {'movieId': 73017, 'title': 'Sherlock Holmes (2009)', 'genres': 'Action|Crime|Mystery|Thriller', 'imdbId': 988045, 'tmdbId': 10528, 'ratings': 14.235805245090482}, {'movieId': 2959, 'title': 'Fight Club (1999)', 'genres': 'Action|Crime|Drama|Thriller', 'imdbId': 137523, 'tmdbId': 550, 'ratings': 3.975187754112997}, {'movieId': 527, 'title': "Schindler's List (1993)", 'genres': 'Drama|War', 'imdbId': 108052, 'tmdbId': 424, 'ratings': 2.7697221727814845}, {'movieId': 356, 'title': 'Forrest Gump (1994)', 'genres': 'Comedy|Drama|Romance|War', 'imdbId': 109830, 'tmdbId': 13, 'ratings': 2.5542273693194986}, {'movieId': 116797, 'title': 'The Imitation Game (2014)', 'genres': 'Drama|Thriller|War', 'imdbId': 2084970, 'tmdbId': 205596, 'ratings': 2.3844371818347643}, {'movieId': 44191, 'title': 'V for Vendetta (2006)', 'genres': 'Action|Sci-Fi|Thriller|IMAX', 'imdbId': 434409, 'tmdbId': 752, 'ratings': 2.3428834133945466}]}


# %%
len(result)
s = set()
l = []
for i in result:
    l.append(i[0])
    print(i)
sorted(l)


# %%
a = [(2959, 3.975187754112997), (2571, 3.1863064439122946), (4993, 3.0730853566355294), (7153, 2.874261116014712), (593, 2.845940435975078), (527, 2.7697221727814845), (356, 2.5542273693194986), (116797, 2.3844371818347643), (44191, 2.3428834133945466), (5952, 2.32666188645332)]
b = [(2959, 19.175608046298752), (122904, 17.22407608875293), (68954, 16.651849160978664), (72998, 15.875093910893185), (109374, 15.191764817053288), (59315, 14.857106275889432), (69122, 14.38128225841483), (73017, 14.235805245090482), (2571, 14.107013048746147), (7153, 13.991967867580199)]
sorted(a + b)


# %%
import re
pat1 = re.compile('Grumpier')
pat2 = re.compile('.*(Romance).*')
condition = {
    'title': pat1,
    'genres': pat2,
}
condition


# %%
for i in database.movies.find(condition):
    print(i)


# %%

keyword = "zhang"
condition = {}
condition['$regex'] = keyword
condition


# %%
str = re.compile('com')
res = database.movies.find({
    '$or': [
        {'title': str},
        {'genres': str}
    ]
},
{
    '_id':0
}
)
for i in res :
    print(i)


# %%
a = {}
d = database.links.find_one({
    'movieId':1,
},{
    "_id": 0,
    "imdbId":1,
    'tmdbId':1,
})
a.update(d)
a


# %%
data = {
 'userId': 1,
 'movies': [{'movieId': 589,
   'title': 'Terminator 2: Judgment Day (1991)',
   'genres': 'Action|Sci-Fi',
   'imdbId': 103064,
   'tmdbId': 280,
   'ratings': 6.162095770830263},
  {'movieId': 924,
   'title': '2001: A Space Odyssey (1968)',
   'genres': 'Adventure|Drama|Sci-Fi',
   'imdbId': 62622,
   'tmdbId': 62,
   'ratings': 5.85024663310409},
  {'movieId': 1036,
   'title': 'Die Hard (1988)',
   'genres': 'Action|Crime|Thriller',
   'imdbId': 95016,
   'tmdbId': 562,
   'ratings': 5.8399580932363495},
  {'movieId': 1200,
   'title': 'Aliens (1986)',
   'genres': 'Action|Adventure|Horror|Sci-Fi',
   'imdbId': 90605,
   'tmdbId': 679,
   'ratings': 5.833714687702518},
  {'movieId': 1391,
   'title': 'Mars Attacks! (1996)',
   'genres': 'Action|Comedy|Sci-Fi',
   'imdbId': 116996,
   'tmdbId': 75,
   'ratings': 5.485294588525373}]
}


# %%
import pymongo
uri = 'mongodb://root:root@192.168.43.184:27017'
database = pymongo.MongoClient(uri).chapter_4
handler = database.user_rec_cache
post_id = handler.insert_one(data).inserted_id


# %%
data = handler.find({}).limit(10)

l = []
for i in data:
    l.append(i)
# l = list(data)
l[-1]


# %%
handler.update_many({},{
    '$set':{
        'no':1
    }
}


# %%
data = handler.find({})


# %%
len(list(data))


# %%
b = [x for x in range(10)]
from collections import Iterable
isinstance(iter(b), Iterable)

type(b)


# %%
import re
title = ".*{0}.*".format("2017")
condition = re.compile(title)
movie_list = database.movies.find({
    '$or': [
        {'title': condition},
        {'genres': condition},
    ]
},
    {
        '_id': 1
    }
)
for i in movie_list:
    print(i.get('_id'))


# %%

def movie_extend(movie_list):
    result = []
    for i in movie_list:
        d = i.copy()
        t = database.links.find_one({
            'movieId': i.get('movieId')
        },
            {
                "_id": 1,
                "imdbId": 1,
                "tmdbId": 1,
            }
        )
        try:
            d.update(t)
        except TypeError:
            continue
        except BaseException:
            continue
        result.append(d)
    # database.movies_cache.insert_many(result)
    print(result)

# %% [markdown]
# # 播放记录

# %%
# 播放记录
base_data = database.ratings.find({
    'user':1
})
extent_data = []
for i in base_data:
    tmp = i.copy()
    movie = database.movies.find_one({
        'movieId':i.get('movie')
    },{
        '_id':0
    })
    user = database.user_detail.find_one({
        'userId':i.get('user')
    },{
        '_id':0,
        'username':1
    })
    # print(movie)
    tmp['movie'] = movie
    tmp['user'] = user.get('username')
    extent_data.append(tmp)
    # print(type(i))
print(extent_data[0])


# %%



# %%
import logging
logging.warning("now")
# log = Logger("now")
# log.info(name="nsd", msg='12')

# %% [markdown]
# 修改用户信息

# %%
base_user = database.user_detail.find_one({
    'userId':1
})
base_user
new_user = {
    'userId':1,
    'pwd': 1234
}
base_user.update(new_user)
base_user
x = database.user_detail.replace_one(base_user,new_user)
x


# %%
{'_id': ObjectId('60b0472d0c95ecbd40d27fa6'),
 'userId': 1.0,
 'name': 'braund',
 'username': 'Braund',
 'pwd': 1234}


# %%



# %%
{'_id': ObjectId('60ae1442ea5ac91e15b739b8'), 'user': 1, 'movie': 1, 'rating': 4.0, 'movie_detail': {'movieId': 1, 'title': 'Toy Story (1995)', 'genres': 'Adventure|Animation|Children|Comedy|Fantasy'}}
播放记录格式


# %%
in(post_id)


# %%
database.list_collection_names()


# %%
from bson.objectid import ObjectId

handler.find_one({
    'id':ObjectId('60af51d07b29b12ecbce2b99')
    })


# %%
def log(func):
    def wap(*args, **kw):
        print("call %s()" % func.__name__)
        return func(*args, **kw)
    return wap

@log
def now():
    print("2012")
now()


# %%
base_user = database.user_detail.find({
    
})

for i in base_user:
    print(i)
    break


# %%
print('hello')

# %% [markdown]
# ## 电影信息

# %%
movie_link = {}

for i in  database.links.find({

},{
    '_id':0
}):
    movie_link.setdefault(i.get('movieId'), i)

# for k,v in movie_link.get(1).items():
#     print(k, v)
movie_link.get(1)

# %% [markdown]
# 电影信息统计

# %%
import pandas as pd 


# %%
movie_total = {}

for data in database.ratings.find({}):
    movie_total.setdefault(data.get('movie'),0)
    movie_total[data.get('movie')] += 1
# print(movie_total.get())

movies = database.movies.find({})


movie_link = {}
for i in  database.links.find({

},{
    '_id':0
}):
    movie_link.setdefault(i.get('movieId'), i)

movie_detail = []
for i in movies:
    i.setdefault('movie_total', 0)
    i['movie_total'] = movie_total.get(i.get('movieId',0))
    i.setdefault('movie_link', None)
    i['movie_link'] = movie_link.get(1)
    # print(movie_total[i.get('movieId')])
    movie_detail.append(i)
    


# %%
type(movies)
for i in movie_detail:
    print(i)
    break


# %%
for i in movie_total.items():
    print(i)
    break


# %%
{'_id': ObjectId('60ae14d380fa7cac904b802a'), 'movieId': 1, 'title': 'Toy Story (1995)', 'genres': 'Adventure|Animation|Children|Comedy|Fantasy', 'movie_total': 215}

# %% [markdown]
# 电影相似度缓存

# %%
import redis
client = redis.Redis(host="192.168.43.184",username="root",password=1234)
int(client.get(1))


# %%
client.set(12,123)

type((client.get(12)))


# %%
import csv 
app = []
with open('movies.csv', 'r', encoding='utf8') as csvfile:
    head = csv.DictReader(csvfile)
    for i in head:
        app.append(i)
len(app)


# %%

def read_csv():
    with open('movies.csv', 'r', encoding='utf8') as csvfile:
        head = csv.reader(csvfile)
        for i in head:
            yield i
list_d = []
for movieId, title, genres in read_csv():
    try:
        list_d.append({
            'movieId':int(movieId),
            'title':title,
            'genres':genres,
        })
    except ValueError:
        continue

database.movies.insert_many(list_d)



# %%
