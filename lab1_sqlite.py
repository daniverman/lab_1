import sqlite3
from flask import Flask
from flask import jsonify
from flask import request
#2
app = Flask(__name__)


def create_table():
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS store (item TEXT,quantity INTEGER,price REAL)")
    conn.commit()
    conn.close()


def insert(item, q, p):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO store  VALUES (?,?,?);", (item, q, p))
    conn.commit()
    conn.close()


@app.route('/',methods=['GET','POST'])
def view():
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("SELECT * FROM store;")
    rows = cur.fetchall()
    for row in rows:
        print row
    return jsonify(rows)


def delete(item):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("DELETE FROM store WHERE item=?", (item,))
    conn.commit()
    conn.close()


def update(q, p, item):
    conn = sqlite3.connect('lite.db')
    cur = conn.cursor()
    cur.execute("UPDATE store SET quantity=?, price=? WHERE item=?;", (q, p, item))
    conn.commit()
    conn.close()



if __name__=='__main__':
    app.run(debug=True)
