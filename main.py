from flask import Flask
from flask import render_template, redirect, request, url_for, session
import sqlite3
import os
from flask import g

DATABASE = 'database.db'

app = Flask(__name__)
app.config["SECRET_KEY"] = os.urandom(16)

if __name__ == "__main__":
    app.run()

@app.before_request
def make_session_permanent():
    session.permanent = True

def init_db(): #create db schema to schema.sql
    with app.app_context(): 
        db = get_db() 
        with app.open_resource('schema.sql', mode='r') as f: 
            db.cursor().executescript(f.read())
        db.commit()

def get_db(): 
    db = getattr(g, '_database', None)
    if db is None: 
        db = g._database = sqlite3.connect(DATABASE, isolation_level=None)
    db.row_factory = sqlite3.Row
    return db

def get_all():
    query = "SELECT * FROM pastes WHERE private_paste = 'False';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close() 
    print(rv)
    return rv

def get_paste(id, args=(), one=False): 
    query = "SELECT * FROM pastes WHERE id = '" + str(id) + "';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

def save_paste_to_db(query, args=(), one=False):
    cur = get_db().execute(query)
    cur.close()

def user_credentials(username): 
    query = "SELECT * FROM 'users' WHERE user = '" + str(username) + "';"
    print(query)
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close() 
    return rv

def add_user(username, pw, email="Null"): 
    query = "INSERT INTO users (user, pw, email) VALUES ('" + username + "', '" + pw + "', '" + email + "');"
    try: 
        cur = get_db().execute(query)
        cur.close()
    except: 
        print("error")

def get_user_pastes(username): 
    query = "SELECT * FROM pastes WHERE user='" + str(username) + "';"
    cur = get_db().execute(query)
    rv = cur.fetchall()
    cur.close()
    return rv

@app.teardown_appcontext
def close_connection(exception): 
    db = getattr(g, '_database', None)
    if db is not None: 
        db.close()

@app.route('/')
def index(): 
    if 'user' in session: 
        user = session['user']
        return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user=user)
    else:
        user = 'Not logged in'
    
    return render_template("index.html", pastes=get_all(), user=user)

@app.route('/form')
def form(): 
    text = request.args.get('text')
    is_private = request.args.get('private') != None
    if 'user' in session:
        user = session['user']
    else: 
        user = 'Not logged in'

    query = "INSERT INTO pastes (body, private_paste, user) VALUES ('" + text + "', '" + str(is_private) + "', '" + user + "');"
    print(query)
    try: 
        save_paste_to_db(query)
    except: 
        print("Error.")
    return redirect(url_for('index'))

@app.route('/paste/')
def paste():
    id = request.args.get('paste')
    paste = get_paste(id, 0)
    if 'user' in session:
        return render_template("index.html", paste=paste, pastes=get_all(), user_pastes=get_user_pastes(session['user']), user=session['user'])
    else: 
        user = "Not logged in"

    return render_template("index.html", paste=paste, pastes=get_all(), user=user)

@app.route('/login', methods=['POST'])
def login(): 
    user = str(request.form.get('user'))
    pw = str(request.form.get('pw'))
    credentials = user_credentials(user)
    error = "None"

    if not user: 
        error = 'Username is empty.'
    elif not pw: 
        error = 'Password is empty.'

    if credentials:
        credentials = credentials[0]
        login_user = credentials[0]
        login_pw = credentials[1]
        if 'user' not in session:
            if user == login_user and pw == login_pw:
                session['user'] = user
                return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user=login_user)
        else: 
            return redirect(url_for('index'))

    else: 
        if 'user' not in session: 
                add_user(user, pw)
                session['user'] = user
                return redirect(url_for('index'))
        else: 
            return render_template("index.html", pastes=get_all(), user_pastes=get_user_pastes(user), user=login_user)


@app.route('/logout')
def logout(): 
    session.pop('user', None)
    return redirect(url_for('index'))