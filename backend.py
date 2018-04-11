import os.path
import sqlite3
import csv


# check if db exist
def check_if_db_exist():
    path = os.getcwd() + "\\db.db"
    return True if os.path.exists(path) else False


def load_movie_file():
    with open("movies.csv") as csvfile:
        movies = csv.reader(csvfile,delimiter=' ', quotechar='|')
        for row in movies:
            ""



# build the data base
def build_db():
    if check_if_db_exist():
        return
    else:
        movies = load_movie_file()
