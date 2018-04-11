import sqlite3


def create_table():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS movies (ID PRIMARY KEY ,Title TEXT,Genre TEXT)")
    conn.commit()
    conn.close()


def insert(*args):
    ID = args[0]
    Title = args[1]
    Genre = args[2]
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO movies  VALUES (?,?,?);", (ID, Title, Genre))
    conn.commit()
    conn.close()


def select_all():
    conn = sqlite3.connect('db.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM movies;")
    items=cur.fetchall()
    conn.commit()
    conn.close()

    return items



