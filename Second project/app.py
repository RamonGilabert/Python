import sqlite3
from flask import Flask, request, session, g, \
redirect, url_for, abort, render_template
from connection import Connection

DATABASE = '/tmp/users.db'
SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'
MESSAGE = None
ERROR = None

app = Flask(__name__)
app.config.from_object(__name__)
connection = Connection(app)

@app.before_request
def before_request():
    g.db = connection.connect_database()

@app.teardown_request
def teardown_request(exception):
    db = getattr(g, 'db', None)
    if db is not None:
        db.close()

@app.route("/")
def main_view():
    sending = app.config['MESSAGE']
    app.config['MESSAGE'] = None
    return render_template("index.html", message=sending)

@app.route("/insert_user")
def insert_view():
    sending = app.config['ERROR']
    app.config['ERROR'] = None
    return render_template("insert.html", error=sending)

@app.route("/post_user", methods=['POST', 'GET'])
def post_new_user():
    username = request.form['username']
    fields = [username, request.form['name'], request.form['email'], request.form['password']]

    for field in fields:
        if not field:
            error = 'You have some blank fields. Check them and submit again.'
            app.config['ERROR'] = error
            return redirect(url_for('insert_view'))
            abort(400)

    execution = g.db.execute('SELECT * FROM Users')
    usernames = [row[1] for row in execution.fetchall()]

    if username in usernames:
        error = 'This username is being used already.'
        app.config['ERROR'] = error
        return redirect(url_for('insert_view'))
        abort(400)

    g.db.execute('INSERT INTO Users (username, name, email, password) VALUES (?, ?, ?, ?)', fields)
    g.db.commit()

    app.config['MESSAGE'] = 'Your new user has been added.'
    return redirect(url_for('show_users'))

@app.route("/show_users")
def show_users():
    sending = app.config['MESSAGE']
    app.config['MESSAGE'] = None
    return render_template('show.html', users=connection.get_users(), message=sending)

@app.route("/login")
def login_view():
    sending_error = app.config['ERROR']
    sending_message = app.config['MESSAGE']
    app.config['ERROR'] = None
    app.config['MESSAGE'] = None
    return render_template("login.html", error=sending_error, message=sending_message)

@app.route("/login_user", methods=['POST'])
def login():
    error = None
    if not request.form['username']:
        error = 'Your username cannot be blank.'
    elif not request.form['password']:
        error = 'Your password cannot be blank.'
    elif request.form['username'] != app.config['USERNAME']:
        error = 'Invalid username.'
    elif request.form['password'] != app.config['PASSWORD']:
        error = 'Invalid password.'

    if error == None:
        session['logged_in'] = True
        app.config['MESSAGE'] = 'You are now logged in.'
        return redirect(url_for('main_view'))

    app.config['ERROR'] = error
    app.config['MESSAGE'] = message
    return redirect(url_for('login_view'))
    abort(401)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('logged_in', None)
    app.config['MESSAGE'] = 'You are now logged out.'
    return redirect(url_for('main_view'))

if __name__ == "__main__":
    connection.init_database()
    app.run()
