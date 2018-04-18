import os.path
import sqlite3
import csv
import math
import db as db
import operator

from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)


def build_rating_in_db():
    if check_if_db_exist("rating_db.db") is False:
        to_db = None
        with open("ratings.csv") as csvfile:
            dr = csv.DictReader(csvfile)
            to_db = [(i['userId'], i['movieId'], i['rating'], i['timestamp']) for i in dr]
        db.create_rating_table()
        db.insert_ratings(to_db)
    else:
        return


def check_if_db_exist(db_name):
    path = os.getcwd() + "\\" + db_name
    return True if os.path.exists(path) else False


# check if db exist


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


def insert_movies_to_db():
    to_db = None
    with open('movies.csv', 'rb') as fin:
        dr = csv.DictReader(fin)
        to_db = [(i['movieId'], i['title'], i['genres'].split('|')[0]) for i in dr]
    db.load_db(to_db)


# build the data base
def build_db():
    # ratings_list = load_rating_file_to_list()

    if check_if_db_exist("db.db"):
        return
    else:
        # movies = load_movie_file()
        db.create_table()
        insert_movies_to_db()


# def load_rating_file_to_list():
#     toReturn = []
#     with open("ratings.csv") as csvfile:
#         ratings = csv.reader(csvfile)
#         # junk = ratings.next()
#         for row in ratings:
#             user_id = row[0]
#             movie_id = row[1]
#             rating = row[2]
#             timestamp = row[3]
#             ratings_list.append(user_id)
#             ratings_list.append(movie_id)
#             ratings_list.append(rating)
#             ratings_list.append(timestamp)
#     return toReturn


def get_all_movies():
    return db.select_all()


def get_movie(*tuples):
    args = []
    for tuple in tuples:
        args.append(tuple) if tuple[0] is not "" else None
    ans = db.select(args)
    return ans


def add_movie(*tuples):
    movies_data = []
    for tuple in tuples:
        movies_data.append(tuple) if tuple[0] is not "" else None
    db.insert(movies_data)


def update_movie(old_id, new_id, new_title, new_genre):
    db.update(old_id, new_id, new_title, new_genre)


def delete_movie(id):
    db.delete(id)


def extract_movie_list(user_movie_list_and_ratings):
    ans = [x[0] for x in user_movie_list_and_ratings]
    return ans


def calculate_avg_rating(user_movie_list_and_ratings):
    avg = 0.0
    for tuple in user_movie_list_and_ratings:
        avg += float(tuple[1])
    return avg / user_movie_list_and_ratings.__len__()


def order_users_movie_and_rating_list(users_movie_list_and_ratings_rows):
    dic = {}
    for tuple in users_movie_list_and_ratings_rows:
        id = tuple[0]
        movie_id = tuple[1]
        rating = tuple[2]
        if dic.has_key(id):
            dic[id].append([movie_id, rating])
        else:
            dic[id] = [[movie_id, rating]]
    return dic


def calculate_avg_rating_and_extract_movie_list(users_movie_list_and_ratings):
    ans = {}
    for user in users_movie_list_and_ratings.iterkeys():
        avg = calculate_avg_rating(users_movie_list_and_ratings[user])
        list = extract_movie_list(users_movie_list_and_ratings[user])
        ans[user] = [avg, list]
    return ans


def intersection(user_list, other_user_list):
    return set.intersection(set(user_list), set(other_user_list))


def calculate_sim(user_id):
    sim_dic = {}
    # get data from db
    user_movie_list_and_ratings = db.get_user_movie_list_and_ratings(user_id)
    user_movie_and_ratings_dic = dict(user_movie_list_and_ratings)
    users_movie_list_and_ratings_rows = db.get_all_user_movie_list_and_ratings(user_id)
    # extract what needed before calculation
    users_movie_list_and_ratings = order_users_movie_and_rating_list(users_movie_list_and_ratings_rows)
    user_movie_list = extract_movie_list(user_movie_list_and_ratings)
    user_avg_rating = calculate_avg_rating(user_movie_list_and_ratings)
    users_movie_list_and_avg_dic = calculate_avg_rating_and_extract_movie_list(users_movie_list_and_ratings)
    # start fill the sim_dic
    for user in users_movie_list_and_avg_dic.iterkeys():
        same_movies = []
        same_movies = intersection(user_movie_list, users_movie_list_and_avg_dic[user][1])
        if len(same_movies) > 0:
            users_movie_and_rating_dic = dict(users_movie_list_and_ratings[user])
            sim = 0.0
            numerator, denominator, denominator1, denominator2, temp1, temp2 = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
            for movie in same_movies:
                temp1 = (float(user_movie_and_ratings_dic[movie]) - user_avg_rating)
                temp2 = (float(users_movie_and_rating_dic[movie]) - float(users_movie_list_and_avg_dic[user][0]))
                numerator += (temp1 * temp2)
                denominator1 += math.pow(temp1, 2)
                denominator2 += math.pow(temp2, 2)
            denominator = math.sqrt(denominator1) * math.sqrt(denominator2)
            denominator = 0.1 if denominator == 0 else denominator
            sim = numerator / denominator
            sim_dic[user] = sim
        else:
            sim_dic[user] = 0
    return sim_dic


def sort_movie_list_by_ratings(movie_rating_list):
    pass


def get_top_k_users(sorted_sim_dic):
    pass


def get_movie_names_from_id(id_list):
    ans = []
    for id in id_list:
        ans.append(db.get_movie_name_from_id(id)[0][0])
    return ans


def check_if_user_exist(user_id):
    return True if len(db.check_if_user_exist(user_id)) else False


def ger_k_rec(user_id, k_rec):
    if check_if_user_exist(user_id):
        movie_id_dic = {}
        sim_dic = calculate_sim(user_id)
        sorted_sim_list = sorted(sim_dic.iteritems(), key=lambda (k, v): v, reverse=True)
        top_k_users = dict(sorted_sim_list[0:k_rec:1])
        for user in top_k_users.iterkeys():
            movie_rating_list = db.get_user_movie_list_and_ratings(user)
            movie_rating_list.sort(key=lambda x: x[1], reverse=True)
            for movie in movie_rating_list:
                if movie_id_dic.has_key(movie[0]) is False:
                    movie_id_dic[movie[0]] = True
                    break

        return get_movie_names_from_id(movie_id_dic.viewkeys())
    else:
        return ["no user id exist"]


@app.route('/rec/', methods=['GET', 'POST'])
def handle_request():
    if request.method == 'POST':
        try:
            data = request.get_json()
            user_id = data['userid']
            k_rec = data['k']
            k_list = ger_k_rec(user_id, k_rec)
            return jsonify(k_list)
        except:
            user_id, k_rec = None

    elif request.method == 'GET':
        try:
            user_id = request.args.get("userid")
            k_rec = int(request.args.get("k"))
            k_list = ger_k_rec(user_id, k_rec)
            return jsonify(k_list)
        except:
            user_id, k_rec = None
    return jsonify("Missing parameters")


if __name__ == '__main__':
    build_rating_in_db()
    app.run(debug=True)
