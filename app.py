from flask import Flask, request, \
    render_template, redirect, url_for, send_from_directory, session
import json
import datetime
import hashlib
import time
from urllib.parse import quote, unquote
import os
from flask_cors import *
import re
from db.init_data import data as tmp
from db.page import get_page
from Recommend import get_movies_cache, valid_logined, valid_logout, \
    search_movies, is_login, valid_sign, search_movies_extention, valid_change_pwd
from count import get_user_detail, movie_detail, movie_record, user_record, \
    count_table, count_user_table
from db.redisUtil import RedisUtil
# from your_code_here.RedisUtil import RedisUtil

app = Flask(__name__)
# 设置跨域
CORS(app, supports_credentials=True)
app.secret_key = os.urandom(10)


redis_util = RedisUtil()


@app.route('/test')
def show():
    """
    测试页面用
    :return: 待预览页面
    """
    return render_template('user_dashboard.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    page_info = get_page(request)
    if is_login(request, session):
        return render_template('dashboard.html',
                               page_info=page_info)


# 电影网站主页
@app.route("/", methods=['GET', 'POST'])
def index():
    page_info = get_page(request)
    if is_login(request, session):
        # 登录验证
        coo_user_id = int(request.cookies.get('login_id'))

        if "user_id" in session:
            ses_user_id = int(session['user_id'])

        if ses_user_id == coo_user_id:
            data = get_movies_cache(ses_user_id).get("movies", tmp)
        else:
            return redirect('/logout')
        # 右边的排行榜
        top_tmp_movie = movie_detail(1,10)
        movie_rec = get_movies_cache(ses_user_id)
        return render_template("index2.html",
                               username=request.cookies.get('username'),
                               movie=movie_rec.get(ses_user_id),
                               top_movie=top_tmp_movie,
                               page_info=page_info
                               )

    return redirect('login')


# 退出登录 清除session
@app.route("/logout", methods=['GET'])
def logout():
    token = session['token_pwd']
    # 清除 session
    session.pop('username', None)
    session.pop('token_pwd', None)
    # 清除缓存数据库
    valid_logout(token)
    return redirect(url_for('index'))


@app.route('/valid_name', methods=['POST'])
def login_name():
    """验证用户可用否"""
    request.form.get('username')
    request_data = request.json
    username = request_data.get('username', '')

    if redis_util.is_nick_already_exists(username) and username is not None:
        return json.dumps({'success': False,
                           'reason': '昵称：{nick}已经被人占用！'.format(nick=username)},
                          ensure_ascii=False)

    return json.dumps({
        'success': True,
        'reason': '用户名{0}可用'.format(username)
    })


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_name = request.form['username']
        user_pwd = request.form['password']

        status = valid_logined(user_name, user_pwd)

        if status:
            redirect_to_index = redirect('/')
            resp = app.make_response(redirect_to_index)
            # 设置cookie
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


@app.route('/change_pwd', methods=['GET', 'POST'])
def change_pwd():
    """
    注册功能
    :return:
    """
    if request.method == 'POST':

        user_dict = request.form.to_dict()
        status = valid_change_pwd(user_dict, user_dict)
        # print(user_dict)
        if status:
            return redirect('/login')
        else:
            return render_template('sign.html', error='login failed')

    if request.method == 'GET':
        return render_template('change_pwd.html', forget_pwd=True)




@app.route('/search', methods=['GET', 'POST'])
def search_movie():

    page_info = get_page(request)

    if request.method == "GET":
        word = request.args.get("search_word")
        condition = re.compile('.*{0}.*'.format(word))
        search_data = search_movies(condition, page=page_info.get('page_id'),
                             count=page_info.get('count'))

    if request.method == "POST":
        word = request.args.get("search_word")
        condition = re.compile('.*{0}.*'.format(word))
        search_data = search_movies(condition, page=page_info.get('page_id'),
                                    count=page_info.get('count'))
    return render_template('index2.html', movie=list(search_data),
                           username=request.cookies.get('username'),
                           page_info=page_info)


@app.route('/update/<string:d_type>', methods=['GET', "POST"])
def update_detail(d_type):
    # TODO update 操作 修改数据
    pass


@app.route('/get_total_movie', methods=['GET'])
def get_movie_total():
    page = int(request.args.get('page', 1))
    count = int(request.args.get('count', 20))

    max_total = count_table('ratings', int(page), int(count))
    movie_total_data = movie_detail(page, count)

    return {"data": movie_total_data}



@app.route('/get/<string:d_type>', methods=['GET', "POST"])
def get_detail(d_type):


    page_info = get_page(request)
    page = page_info.get("page_id")
    count = page_info.get('count')

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
        page_info = count_user_table('ratings', page=page, count=count,
                                     user=user_id)

        return render_template("user_record_detail.html", page_info=page_info
                            , username=request.cookies.get('username'),
                               data=user_records, user_record_type=True)

    if "user" == d_type:
        """
        用户信息
        """

        user_data = get_user_detail(index_page=int(page) - 1, count=int(count))

        page_info = count_table('user_detail', page=page, count=count)

        return render_template("user_detail.html",
                               username=request.cookies.get('username'),
                               page_info=page_info, data=user_data,
                               user_type=True)

    if "movie" == d_type:
        """
        电影信息
        """
        movie_details = movie_detail(page=int(page) - 1, count=int(count))
        page_info = count_table('movies', page=page, count=count)

        return render_template("movie_detail.html", data=movie_details,
                               username=request.cookies.get('username'),
                               page_info=page_info,
                               movie_type=True)

    if "movie_url" == d_type:
        """
        电影链接
        """
        # print(url_for('get_detail', d_type='movie_url'))

        data = movie_detail(page=int(page) - 1, count=int(count))
        page_info = count_table('movies', page=page, count=count)

        return render_template("movie_url_edit.html", data=data,
                               username=request.cookies.get('username'),
                               page_info=page_info, movie_url_type=True)

    if "movie_record" == d_type:
        """
        用户电影播放记录
        """
        user_id = int(session['user_id'])
        data = user_record(user_id, page=int(page) - 1, count=int(count))
        page_info = count_table('ratings', page=page, count=count,
                                condition={'user': user_id})

        return render_template('user_dashboard.html', data=data,
                               username=request.cookies.get('username'),
                               page_info=page_info)

    if "movie_total" == d_type:
        return render_template('dashboard.html',
                               username=request.cookies.get('username'),
                               total_type=True, page_info=page)


@app.route('/play')
def play():
    video = 'http://127.0.0.1:5000/video/frame.mp4'
    return render_template('video.html', video_url=video,
                           top_movie=tmp.get(1))


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


@app.route('/room')
def room():
    nick = request.cookies.get('name')
    token = request.cookies.get('token')

    nick = unquote(nick)
    saved_token = redis_util.get_token(nick)
    if token == saved_token:
        return render_template('chatroom.html')
    return redirect('/')


@app.route('/get_chat_list')
def get_chat_list():
    chat_list = redis_util.get_chat_list()
    return json.dumps(chat_list, ensure_ascii=False)


@app.route('/post_message', methods=['POST'])
def post_message():
    message = request.json
    msg = message.get('msg', '')
    nick = message.get('nick', '')
    if not all([msg, nick]):
        return json.dumps({'success': False, 'reason': '昵称或聊天内容为空！'},
                          ensure_ascii=False)

    expire_time = redis_util.get_nick_msg_expire_time(nick, msg)
    if not expire_time:
        message_info = {'msg': message['msg'],
                        'post_time': datetime.datetime.now().strftime(
                            '%Y-%m-%d %H:%M:%S'),
                        'nick': message['nick']}
        redis_util.push_chat_info(message_info)
        redis_util.set_nick_msg_expire_time(nick, msg)
        return json.dumps({'success': True})
    elif expire_time >= 1:
        return json.dumps({'success': False,
                           'reason': '在两分钟内不同发送同样的内容！还剩{expire_time}秒'.format(
                               expire_time=expire_time)},
                          ensure_ascii=False)

# 获取图片
@app.route("/img/<name>")
def get_img(name):
    d = send_from_directory(
        directory=os.path.join(os.path.abspath('.'), 'img\\'),
        filename=name)
    return d


# 获取电影
@app.route("/video/<name>")
def get_video(name):
    d = send_from_directory(
        directory=os.path.join(os.path.abspath('.'), 'video\\'),
        filename=name)
    return d


if __name__ == '__main__':
    app.run()
