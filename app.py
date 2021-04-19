from django.urls import reverse
from flask import Flask, request, render_template, redirect, url_for
from item import Moive, ItemCF
import numpy
from flask_cors import *

from item.ItemCF import ItemBasedCF

app = Flask(__name__)
CORS(app, supports_credentials=True) #设置跨域


@app.route('/')
def hello_world():
    return render_template("index.html")


@app.route('/to_login/<name>', methods=['GET'])
def login_page(name=None):
    return render_template("base/login.html")


@app.route('/get/<int:recommend_id>', methods=['GET', 'POST'])
def get_recommend(recommend_id=None):
    itemCF = ItemCF.ItemBasedCF()
    itemCF.get_dataset('file\\ratings.csv')
    itemCF.build_movie_matrix()
    itemCF.calc_movie_sim()

    movie = Moive.MovieDetails()
    movie.get_movie_data('file\\movies.csv')

    list_item = itemCF.recommend(str(recommend_id))
    print(recommend_id, len(list_item))
    return {"movie":list_item}


@app.route('/user_list/<int:user_id>')
def get_user_list(user_id=None):
    itemCF = ItemCF.ItemBasedCF()
    path = 'file\\ratings.csv'
    movie_path = 'file\\movies.csv'
    itemCF.get_dataset(path)
    movie = Moive.MovieDetails()
    movie.get_movie_data(movie_path)
    # list_item = itemCF.recommend(str(user_id))
    # data = []
    # for movie_id, similar in list_item:
    #     data.append([movie_id, similar, movie.get_title(movie_id)])
    # return render_template("userlist.html", employee=data)
    return {"movie":movie.movie_list}




# 404 error deal
@app.errorhandler(404)
def page_not_found(error):
    return render_template('404.html',error=error)


if __name__ == '__main__':
    app.run()
