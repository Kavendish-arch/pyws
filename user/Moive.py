from item import tool
import shelve
import os
from contextlib import closing


class MovieDetails:
    def __init__(self):
        self.movie_list = {}


    def get_movie_data(self, filename):
        movie_len = 0

        for line in tool.load_file(filename=filename):
            movie_id, title, genres = line[0], line[1], line[2]
            self.movie_list.setdefault(movie_id, {})
            self.movie_list[movie_id].setdefault(title, genres)
            movie_len += 1
        return movie_len


    def get_title(self, movie_id):
        return self.movie_list.get(movie_id)


    def save_data(self):
        with closing(shelve.open('movie_data','c')) as shelf:
            shelf['movie'] = self.movie_list


    def read_data(self):
        with closing(shelve.open('movie_data','r')) as shelf:
            self.movie_list = shelf['movie']


if __name__ == "__main__":
    path = os.path.abspath(os.curdir) + \
           "\\bigdata\\ml-latest-small\\movies.csv"
    movieDetails = MovieDetails()
    movieDetails.get_movie_data(path)
    print(movieDetails.movie_list)

    for i,key in movieDetails.movie_list.items():
        print(i,key)