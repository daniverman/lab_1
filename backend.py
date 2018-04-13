import os.path
import sqlite3
import csv
import db as db


# check if db exist
def check_if_db_exist():
    path = os.getcwd() + "\\db.db"
    return True if os.path.exists(path) else False


def load_movie_file():
    movies_dic = dict()
    with open("movies.csv") as csvfile:
        movies = csv.reader(csvfile)
        junk = movies.next()
        for row in movies:
            id = row[0]
            name = row[1]
            catagory = row[2].split("|")[0]
            movies_dic[id] = (name, catagory)
    return movies_dic


def insert_movies_to_db(movies):
    for movie in movies.iterkeys():
        id = movie
        name = movies[id][0]
        genre = movies[id][1]
        db.insert(id, name, genre)


# build the data base
def build_db():
    if check_if_db_exist():
        return
    else:
        movies = load_movie_file()
        db.create_table()
        insert_movies_to_db(movies)


def get_all_movies():
    return db.select_all()


def get_movie(*tuples):
    args = []
    for tuple in tuples:
        args.append(tuple) if tuple[0] is not "" else None
    ans = db.select(args)
    return ans


def add_movie(*tuples):
    args = []
    for tuple in tuples:
        args.append(tuple) if tuple[0] is not "" else None
    db.insert(args)


def update_movie(old_id, new_id, new_title, new_genre):
    db.update(old_id, new_id, new_title,new_genre)


def delete_movie(id):
    db.delete(id)