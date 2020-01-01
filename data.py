from flask import Flask, g, current_app
import sqlite3

DATABASE = 'database.db'

def get_db():
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    db.row_factory = sqlite3.Row
    return db

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

def read_db(query, params=None):
    if params is not None: 
        cur = get_db().execute(query, params)
    else: 
        cur = get_db().execute(query)
    rv = cur.fetchall() 
    cur.close()
    return rv

def write_db(query, params=None):
    try: 
        if params is not None: 
            cur = get_db().execute(query, params)
        else: 
            cur = get_db().execute(query)
        cur.close()
    except: 
        print("error")

def get_all():
    return read_db("SELECT * FROM pastes WHERE private_paste = 'False';")

def get_paste(id, user='Not logged in'): 
    if user is 'Not logged in': 
        query = "SELECT * FROM pastes WHERE id = ?;"
        return read_db(query, [id])
    else: 
        query = "SELECT * FROM pastes WHERE id = ? AND (user = ? OR private_paste = 'False');"
        return read_db(query, [id, user])

def save_paste_to_db(text, is_private, user):
    query = "INSERT INTO pastes (body, private_paste, user) VALUES (?, ?, ?);"
    write_db(query, [text, str(is_private), user])

def user_credentials(username): 
    query = "SELECT * FROM 'users' WHERE user = ?;"
    return read_db(query, [username])

def add_user(username, pw, email="Null"): 
    query = "INSERT INTO users (user, pw, email) VALUES (?, ?, ?);"
    write_db(query, [username, pw, email])

def get_user_pastes(username): 
    query = "SELECT * FROM pastes WHERE user=?;"
    return read_db(query, [username])