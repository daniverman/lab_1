import sqlite3


def create_table():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (Id PRIMARY KEY ,Title TEXT,Genre TEXT)")
    conn.commit()
    conn.close()


def insert(*args):
    id, title, genre = '', '', ''
    for arg in args[0]:
        if arg[1] == "id":
            id = arg[0]
        elif arg[1] == "title":
            title = arg[0]
        elif arg[1] == "genre":
            genre = arg[0]
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO movies  VALUES (?,?,?);", (id, title, genre))
    conn.commit()
    conn.close()


def select_all():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    items = cur.fetchall()
    conn.close()
    return items


def select(args):
    id, title, genre = '%', '%', '%'
    for arg in args:
        if arg[1] == "id":
            id = arg[0]
        elif arg[1] == "title":
            title = '%' + arg[0] + '%'
        elif arg[1] == "genre":
            genre = arg[0]
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies WHERE Id LIKE (?) AND Title LIKE (?) AND Genre LIKE (?);", (id, title, genre))
    item = cur.fetchall()
    conn.commit()
    conn.close()
    return item


def update(old_id, new_id, new_title, new_genre):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("UPDATE movies SET Id = (?) ,Title=(?), Genre = (?) WHERE Id=(?);",
                (new_id, new_title, new_genre, old_id))
    conn.commit()
    conn.close()


def delete(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM movies WHERE Id=(?);", (id,))
    conn.commit()
    conn.close()


def load_db(to_db):
    conn = sqlite3.connect('db.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("INSERT INTO movies  VALUES (?,?,?);", to_db)
    conn.commit()


def create_rating_table():
    conn = sqlite3.connect('rating_db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS ratings (userId TEXT,movieId TEXT,rating TEXT ,timestamp TEXT)")
    conn.commit()
    conn.close()


def insert_ratings(to_db):
    conn = sqlite3.connect('rating_db.db')
    conn.text_factory = str
    cur = conn.cursor()
    cur.executemany("INSERT INTO ratings  VALUES (?,?,?,?);", to_db)
    conn.commit()


def get_user_movie_list_and_ratings(user_id):
    conn = sqlite3.connect('rating_db.db')
    cur = conn.cursor()
    cur.execute("SELECT movieId,rating FROM ratings WHERE userId=(?);", (user_id,))
    item = cur.fetchall()
    conn.commit()
    conn.close()
    return item


def get_all_user_movie_list_and_ratings(user_id):
    conn = sqlite3.connect('rating_db.db')
    cur = conn.cursor()
    cur.execute("SELECT userId,movieId,rating FROM ratings WHERE NOT userId=(?);", (user_id,))
    item = cur.fetchall()

    conn.commit()
    conn.close()
    return item


def get_movie_name_from_id(id):
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT Title FROM movies WHERE Id = (?) ;", (id,))
    item = cur.fetchall()
    conn.commit()
    conn.close()
    return item


def check_if_user_exist(user_id):
    conn = sqlite3.connect('rating_db.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM ratings WHERE userId=(?);", (user_id,))
    item = cur.fetchall()
    conn.commit()
    conn.close()
    return item