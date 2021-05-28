from flask import Flask, request, \
    render_template, redirect, url_for, send_from_directory, session

import os
from flask_cors import *
import re
from db.init_data import data as tmp
from Recommend import get_movies_cache, valid_logined,\
    search_movies, is_login, valid_sign
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
    return render_template('lunbo.html')


# 电影网站主页
@app.route("/", methods=['GET', 'POST'])
def index():
    if is_login(request, session):
        user_id = request.cookies.get('login_id')
        if "user_id" in session:
            user_id = int(session['user_id'])
        data = get_movies_cache(user_id)
        return render_template("index2.html",
                               username=request.cookies.get('username'),
                               movie=data.get('movies'), top_movie=tmp.get(1))
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
            session['user_id'] = status.get('login_id')
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

    return render_template('index2.html', movie=list(data))


@app.route('/user_list/<int:user_id>')
def get_user_list(user_id=None):
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
