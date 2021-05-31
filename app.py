from flask import Flask, request, \
    render_template, redirect, url_for, send_from_directory, session

import os
from flask_cors import *
import re
from db.init_data import data as tmp
from Recommend import get_movies_cache, valid_logined, \
    search_movies, is_login, valid_sign, search_movies_extention
from count import get_user_detail, movie_detail, movie_record, user_record,\
    count_table, count_user_table
app = Flask(__name__)
# 设置跨域
# CORS(app, supports_credentials=True)
app.secret_key = os.urandom(10)


@app.route('/test')
def show():
    """
    测试页面用
    :return: 待预览页面
    """
    return render_template('dashboard.html', data=None)


# 电影网站主页
@app.route("/", methods=['GET', 'POST'])
def index():
    if is_login(request, session):

        # 登录验证
        cookie_token = request.cookies.get('token_pwd')
        session_token = session['token_pwd']
        if session_token is None:
            # 数据库中查询
            from db.redisUtil import client
            if client.exists(cookie_token):
                session_token
            pass
        if cookie_token == session_token:
            print("token 验证通过")
        user_id = request.cookies.get('login_id')
        if "user_id" in session:
            user_id = int(session['user_id'])
        data = get_movies_cache(user_id)
        return render_template("index2.html",
                               username=request.cookies.get('username'),
                               movie=data.get('movies'), top_movie=tmp.get(1),
                               )
        # return render_template('index2.html', title=data, movie=data.get(1))

    return redirect('login')


@app.route("/img/<name>")
def get_img(name):
    d = send_from_directory(
        directory=os.path.join(os.path.abspath('.'), 'img\\'),
        filename=name)
    return d


@app.route("/video/<name>")
def get_video(name):
    d = send_from_directory(
        directory=os.path.join(os.path.abspath('.'), 'video\\'),
        filename=name)
    return d


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
            session['user_id'] = status.get('login_id')
            session['token_pwd'] = status.get('token_pwd')
            return resp

        else:
            return render_template('login.html', error='login failed')

    if request.method == 'GET':
        return render_template('login.html', login_page=True)


@app.route('/sign', methods=['GET', 'POST'])
def sign():
    """
    注册功能
    :return:
    """
    if request.method == 'POST':
        user_dict = request.form.to_dict()
        print(user_dict)
        status = valid_sign(user_dict)
        if status:
            return redirect('/login')
        else:
            return render_template('sign.html', error='login failed')

    if request.method == 'GET':
        return render_template('sign.html', sign_page=True)


@app.route('/search', methods=['GET', 'POST'])
def search_movie():
    if request.method == "GET":
        word = request.args.get("search_word")
        condition = re.compile('.*{0}.*'.format(word))
        data = search_movies(condition)

    if request.method == "POST":
        title_world = request.form.get('title')
        genre_world = request.form.get('genre')
        year_world = request.form.get('year')
        data = search_movies_extention(title=title_world,
                                       genre=genre_world, year=year_world)
    return render_template('index2.html', movie=list(data))


@app.route('/update/<string:d_type>', methods=['GET', "POST"])
def update_detail(d_type):
    # TODO update 操作 修改数据
    pass


@app.route('/get/<string:d_type>', methods=['GET', "POST"])
def get_detail(d_type):
    page = request.args.get("page")
    count = request.args.get("count")

    try:
        page = int(page)
        count = int(count)
    except TypeError:
        page = 1
        count = 30
    except ValueError:
        page = 1
        count = 30


    page_info = {
        'min_page_index': 1,
        'max_page_index': 10,
        'page_id': page,
        'count': count,
    }

    # TODO 创建 数据获取
    if "u_record" == d_type:
        """
        用户历史记录
        """
        try:
            user_id = int(request.args.get('user_id'))
        except TypeError:
            user_id = ''
            pass
        except ValueError:
            user_id = ''
            pass
        # user_id = 2
        user_records = user_record(user_id, page=page, count=count)
        page_info = count_user_table('ratings', page=page, count=count, user=user_id)


        return render_template("user_record_detail.html", page_info=page_info
                               , data=user_records, user_record_type=True)


    if "user" == d_type:
        """
        用户信息
        """

        user_data = get_user_detail(index_page=int(page) - 1, count=int(count))

        page_info = count_table('user_detail', page=page, count=count)

        return render_template("user_detail.html",
                               page_info=page_info, data=user_data,
                               user_type=True)

    if "movie" == d_type:
        """
        电影信息
        """
        movie_details = movie_detail(page=int(page) - 1, count=int(count))
        page_info = count_table('movies', page=page, count=count)

        return render_template("movie_detail.html", data=movie_details,
                               page_info=page_info,
                               movie_type=True)

    if "movie_url" == d_type:
        """
        电影链接
        """
        print(url_for('get_detail', d_type='movie_url'))

        data = movie_detail(page=int(page) - 1, count=int(count))
        page_info = count_table('movies', page=page, count=count)

        return render_template("movie_url_edit.html", data=data,
                               page_info=page_info, movie_url_type=True)

    if "movie_record" == d_type:
        """
        用户电影播放记录
        """
        data = movie_detail(page=int(page) - 1, count=int(count))
        page_info = count_table('movie_detail', page=page, count=count)

        return render_template("movie_url_edit.html", data=data,
                               page_info=page_info, movie_url_type=True)


@app.route('/user_list/<int:user_id>')
def get_user_list(user_id=None):
    return


# TODO 获取相似性数据
def similarity():
    pass


@app.route('/upload', methods=['POST', 'GET'])
def upload():
    # TODO 上传文件进行数据分析
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


@app.errorhandler(500)
def server_error(error):
    data = range(10)
    return render_template('404.html', error=error, data=data)


if __name__ == '__main__':
    app.run()
