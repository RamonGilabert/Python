import sqlite3
from flask import Flask, request, session, g, \
redirect, url_for, abort, render_template, flash
from contextlib import closing

DATABASE = '/tmp/users.db'

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

@app.route("/insert_user", methods=['POST', 'GET'])
def insert_view():
    return render_template("insert.html")

def insert_user():
    if not session.get('logged_in'):
        abort(401)
    g.db.execute('insert into entries (title, text) values (?, ?)',
                 [request.form['title'], request.form['text']])
    g.db.commit()
    flash('New entry was successfully posted')
    return redirect(url_for('show_entries'))

@app.route("/show_users")
def show_users():
    execution = g.db.execute('SELECT * FROM Users')
    users = [dict(name=row[2], email=row[3], username=row[1]) for row in execution.fetchall()]
    return render_template('show.html', users=users)

@app.route("/login", methods=['POST', 'GET'])
def login_view():
    return render_template("login.html")

if __name__ == "__main__":
    init_database()
    app.run()
