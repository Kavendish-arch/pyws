from flask import Flask, request, render_template, redirect

app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/login/<name>')
def login_page(name=None):
    return render_template("login.html", user=name)


@app.route('/hello/<name>')
def hello_name(name=None):
    if request.method == 'GET':
        return \
            '<form action="http://127.0.0.1:5000/forms/peng" method="post"><p>First name: <input type="text" name="fname" /></p> \
    <p>Last name: <input type="text" name="lname" /></p> \
      <input type="submit" value="Submit" /> \
    </form>'
    elif request.method == 'POST':
        return 'hello post'
    return 'Hello World!' + name


@app.route('/get/<int:movie_id>',methods=['GET','POST'])
def hello_int(movie_id=None):
    keyword = request.args.get('enc', '')
    print(keyword)
    return "hello " + str(movie_id)

# 转发重定向
@app.route('/red',methods=['GET','POST'])
def red_test():
    return redirect('/hello/ j')


@app.route('/keng')
def keng():
    return render_template("keng.html")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html', error=error)


@app.route("/static/<username>")
def user_info(username):
    print(username)
    return '用户传入的 {0}'.format(username)


# @app.route('/test')
# def test_url_for():
#     print(url_for('hello_world'))  # 输出：/
#     print(url_for('user_info', username='js/mige'))  # 输出：/user/mige
#     print(url_for('user_info', username='zatan'))  # 输出：/user/zatan
#     print(url_for('test_url_for'))  # 输出：/test
#     # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
#     print(url_for('test_url_for', num=4 ** 2))  # 输出：/test?num=16
#     return 'Test page'


if __name__ == '__main__':
    app.run()
