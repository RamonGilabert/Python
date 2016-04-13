import sqlite3
from flask import Flask, request, session, g, \
redirect, url_for, abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/users.db'
SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])

def init_database():
    with closing(connect_database()) as database:
        with app.open_resource('schema.sql', mode='r') as f:
            database.cursor().executescript(f.read())
            database.commit()

@app.before_request
def before_request():
    g.db = connect_database()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def main_view():
    return render_template("index.html")

@app.route("/insert_user")
def insert_view():
    return render_template("insert.html")

@app.route("/post_user", methods=['POST', 'GET'])
def post_new_user():
    g.db.execute('INSERT INTO Users (username, name, email, password) VALUES (?, ?, ?, ?)',
                 [request.form['username'], request.form['name'], request.form['email'], request.form['password']])
    g.db.commit()
    print 'Your new user has been added.'
    return redirect(url_for('show_users'))

@app.route("/show_users")
def show_users():
    execution = g.db.execute('SELECT * FROM Users')
    users = [dict(name=row[2], email=row[3], username=row[1]) for row in execution.fetchall()]
    return render_template('show.html', users=users)

@app.route("/login")
def login_view():
    return render_template("login.html")

@app.route("/login_user", methods=['POST'])
def login():
    error = None
    if request.form['username'] != app.config['USERNAME']:
        error = 'Invalid username.'
    elif request.form['password'] != app.config['PASSWORD']:
        error = 'Invalid password.'
    else:
        session['logged_in'] = True
        print 'You are logged in.'
        return redirect(url_for('main_view'))

    return redirect(url_for('login_view'))

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('main_view'))

if __name__ == "__main__":
    init_database()
    app.run()
