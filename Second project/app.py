import sqlite3
from flask import Flask, request, session, g, \
redirect, url_for, abort, render_template
from connection import Connection

DATABASE = '/tmp/users.db'
SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'

global message = None
global error = None

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
    sending = global message
    global message = None
    return render_template("index.html", message=sending)

@app.route("/insert_user")
def insert_view():
    sending = global error
    global error = None
    return render_template("insert.html", error=sending)

@app.route("/post_user", methods=['POST', 'GET'])
def post_new_user():
    username = request.form['username']
    fields = [username, request.form['name'], request.form['email'], request.form['password']]

    for field in fields:
        if not field:
            global error = 'You have some blank fields. Check them and submit again.'
            return redirect(url_for('insert_view'))
            abort(400)

    execution = g.db.execute('SELECT * FROM Users')
    usernames = [row[1] for row in execution.fetchall()]

    if username in usernames:
        global error = 'This username is being used already.'
        return redirect(url_for('insert_view'))
        abort(400)

    g.db.execute('INSERT INTO Users (username, name, email, password) VALUES (?, ?, ?, ?)', fields)
    g.db.commit()

    global message = 'Your new user has been added.'
    return redirect(url_for('show_users'))

@app.route("/show_users")
def show_users():
    sending = global message
    global message = None
    return render_template('show.html', users=connection.get_users(), message=sending)

@app.route("/login")
def login_view():
    sending_error = global error
    sending_message = global message
    global error = None
    global message = None
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
        global message = 'You are now logged in.'
        return redirect(url_for('main_view'))

    global error = error
    global message = message
    return redirect(url_for('login_view'))
    abort(401)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.pop('logged_in', None)
    global message = 'You are now logged out.'
    return redirect(url_for('main_view'))

if __name__ == "__main__":
    connection.init_database()
    app.run()
