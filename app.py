from flask import Flask, request, \
    render_template, redirect, url_for, send_from_directory, session

import os
from flask_cors import *

app = Flask(__name__)
# 设置跨域
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(10)


def is_login(req, sess):
    user_name = req.cookies.get('login_user')
    status = req.cookies.get('login_status')
    role = req.cookies.get('login_role')
    user_id = req.cookies.get('login_id')
    if "username" in sess:
        if user_name and status and role and user_id:
            return True
        else:
            return False
    else:
        return False


def valid_logined(user_name, user_pwd):
    print(user_name, user_pwd)
    if True:
        return {
            'username': 'jack',
            'login_user': 'jack',
            'login_status': 'True',
            'login_role': 'admin',
            'login_id': '1',
        }
    else:
        return False


# 电影网站主页
@app.route("/", methods=['GET', 'POST'])
def index():
    data = \
        {1:
             [{'movieId': 2115,
               'title': 'Indiana Jones and the Temple of Doom (1984)',
               'genres': 'Action|Adventure|Fantasy',
               'imdbId': 'http://www.imdb.com/title/tt87469',
               'tmdbId': 'https://www.themoviedb.org/movie/87',
               'ratings': 76.45141047797219},
              {'movieId': 1196,
               'title': 'Star Wars: Episode V - The Empire Strikes Back (1980)',
               'genres': 'Action|Adventure|Sci-Fi',
               'imdbId': 'http://www.imdb.com/title/tt80684',
               'tmdbId': 'https://www.themoviedb.org/movie/1891',
               'ratings': 53.172590388030244},
              {'movieId': 1923,
               'title': "There's Something About Mary (1998)",
               'genres': 'Comedy|Romance',
               'imdbId': 'http://www.imdb.com/title/tt129387',
               'tmdbId': 'https://www.themoviedb.org/movie/544',
               'ratings': 36.032801193125835},
              {'movieId': 1200,
               'title': 'Aliens (1986)',
               'genres': 'Action|Adventure|Horror|Sci-Fi',
               'imdbId': 'http://www.imdb.com/title/tt90605',
               'tmdbId': 'https://www.themoviedb.org/movie/679',
               'ratings': 35.64895451997378},
              {'movieId': 480,
               'title': 'Jurassic Park (1993)',
               'genres': 'Action|Adventure|Sci-Fi|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt107290',
               'tmdbId': 'https://www.themoviedb.org/movie/329',
               'ratings': 34.97835205157789},
              {'movieId': 1380,
               'title': 'Grease (1978)',
               'genres': 'Comedy|Musical|Romance',
               'imdbId': 'http://www.imdb.com/title/tt77631',
               'tmdbId': 'https://www.themoviedb.org/movie/621',
               'ratings': 30.092855674772846},
              {'movieId': 2028,
               'title': 'Saving Private Ryan (1998)',
               'genres': 'Action|Drama|War',
               'imdbId': 'http://www.imdb.com/title/tt120815',
               'tmdbId': 'https://www.themoviedb.org/movie/857',
               'ratings': 30.014776987975168},
              {'movieId': 1036,
               'title': 'Die Hard (1988)',
               'genres': 'Action|Crime|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt95016',
               'tmdbId': 'https://www.themoviedb.org/movie/562',
               'ratings': 29.529508499632268},
              {'movieId': 47,
               'title': 'Seven (a.k.a. Se7en) (1995)',
               'genres': 'Mystery|Thriller',
               'imdbId': 'http://www.imdb.com/title/tt114369',
               'tmdbId': 'https://www.themoviedb.org/movie/807',
               'ratings': 29.282623651730994},
              {'movieId': 2683,
               'title': 'Austin Powers: The Spy Who Shagged Me (1999)',
               'genres': 'Action|Adventure|Comedy',
               'imdbId': 'http://www.imdb.com/title/tt145660',
               'tmdbId': 'https://www.themoviedb.org/movie/817',
               'ratings': 25.84264861921086}
              ]
         }

    if is_login(request, session):
        user_id = request.cookies.get('login_id')
        return render_template("index2.html",
                               username=request.cookies.get('username'),
                               movie=data.get(1))
        # return render_template('index2.html', title=data, movie=data.get(1))

    return redirect('login')


# 退出登录 清除session
@app.route("/logout", methods=['GET'])
def logout():
    session.pop('username', None)

    return redirect(url_for('index'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_pwd = request.form['password']

        status = valid_logined(user_name, user_pwd)
        if status:
            redirect_to_index = redirect('/')
            resp = app.make_response(redirect_to_index)
            for key, value in status.items():
                resp.set_cookie(key=key, value=value, max_age=3600)
            session['username'] = status.get('username')

            return resp

        else:
            return render_template('login.html', error='login failed')

    if request.method == 'GET':
        return render_template('login.html')


def valid_login(req):
    valid_status = req.cookie.get('login_status')

    return render_template("index.html")


@app.route('/get/<int:recommend_id>', methods=['GET', 'POST'])
def get_recommend(recommend_id=None):
    """
    itemCF = ItemCF.ItemBasedCF()
    itemCF.get_dataset('file\\ratings.csv')
    itemCF.build_movie_matrix()
    itemCF.calc_movie_sim()

    movie = Moive.MovieDetails()
    movie.get_movie_data('file\\movies.csv')

    data = []
    list_item = itemCF.recommend(str(recommend_id))
    for movie_id, similar in list_item:
        data.append([movie_id, similar, movie.get_title(movie_id)])
    return {"movie":data, "detail":itemCF.evaluate()}
    """


@app.route('/user_list/<int:user_id>')
def get_user_list(user_id=None):
    # itemCF = ItemCF.ItemBasedCF()
    # path = 'file\\ratings.csv'
    # movie_path = 'file\\movies.csv'
    # itemCF.get_dataset(path)
    # movie = Moive.MovieDetails()
    # movie.get_movie_data(movie_path)
    # # list_item = itemCF.recommend(str(user_id))
    # # data = []
    # # for movie_id, similar in list_item:
    # #     data.append([movie_id, similar, movie.get_title(movie_id)])
    # # return render_template("userlist.html", employee=data)
    # return {"movie":movie.movie_list}
    return


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        base_path = os.path.dirname(__file__)  # 当前文件所在路径
        print(base_path)
        # upload_path = os.path.join(base_path, 'file\uploads',
        #                            secure_filename(f.filename))
        # 注意：没有的文件夹一定要先创建，不然会提示没有该路径
        # f.save(upload_path)
        print("ok")
        return redirect(url_for('upload'))
    print("error")
    return render_template('upload.html')


@app.route("/txt/<path:path>")
def get_file_txt(path):
    """
    获取文件：文本类
    :param path: 文件路径
    :return: 文件
    """
    # return send_from_directory('download', path)
    return "hello"


# 404 error deal
@app.errorhandler(404)
def page_not_found(error):
    data = range(10)
    return render_template('404.html', error=error, data=data)


if __name__ == '__main__':
    app.run()
