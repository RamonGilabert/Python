import sqlite3
from flask import Flask, request, session, g, \
redirect, url_for, abort, render_template
from orm_connection import database_session, init_database
from models import User

# This is the configuration of the database and the admin, you can login with
# the credentials below. The secret key is needed to create a log in system.
DATABASE = '/tmp/users.db'
SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'

# To make it more elegant to present errors or message redirecting in flask,
# I've created those global variables and initialized them to None. Since the
# code will check if they are None, if they are not, they will display the
# message.
global message
global error

message = None
error = None

# Instantiation of the app with the configuration stated above in capital
# letters, with also the connection of the app.
app = Flask(__name__)
app.config.from_object(__name__)

@app.teardown_appcontext
def shutdown_session(exception=None):
    database_session.remove()

# Below we'll define our routes.

# There's a pattern accros the routes, which is getting the global variables
# into scoped variables and then setting them to None again.

@app.route("/")
def main_view():
    global message
    sending = message
    message = None
    return render_template("index.html", message=sending)

@app.route("/insert_user")
def insert_view():
    global error
    sending = error
    error = None
    return render_template("insert.html", error=sending)

@app.route("/post_user", methods=['POST', 'GET'])
def post_new_user():
    global error
    global message

    username = request.form['username']
    fields = [username, request.form['name'], request.form['email'], request.form['password']]

    # This checks if there's some field left empty and if it does it aborts with
    # a bad request from the user, displaying an error.
    for field in fields:
        if not field:
            error = 'You have some blank fields. Check them and submit again.'
            return redirect(url_for('insert_view'))
            abort(400)

    usernames = [user.username for user in User.query.all()]

    # Since the username needs to be unique, we check for that here if it exists
    # already, if it does we show the error in the same view.
    if username in usernames:
        error = 'This username is being used already.'
        return redirect(url_for('insert_view'))
        abort(400)

    # We haven't found any problem, thus, we'll insert the user into the
    # database and commit the result of it.
    user = User(username, fields[1], fields[2], fields[3])
    database_session.add(user)
    database_session.commit()

    message = 'Your new user has been added.'
    return redirect(url_for('show_users'))

@app.route("/show_users")
def show_users():
    global message
    sending = message
    message = None

    return render_template('show.html', users=User.query.all(), message=sending)

@app.route("/login")
def login_view():
    global error
    global message
    sending_error = error
    sending_message = message
    error = None
    message = None
    return render_template("login.html", error=sending_error, message=sending_message)

@app.route("/login_user", methods=['POST'])
def login():
    global error
    global message

    # Similar to the insert view, in here we'll check if first the fields
    # are empty and then if they are the same as the stated in the app
    # configuration. If they are we are going to put in the session of Flask
    # a True flag into the 'logged_in' key.
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
        message = 'You are now logged in.'
        return redirect(url_for('main_view'))

    return redirect(url_for('login_view'))
    abort(401)

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    # We need to change the value of 'logged_in' to none to log out completely.
    session.pop('logged_in', None)
    global message
    message = 'You are now logged out.'
    return redirect(url_for('main_view'))

if __name__ == "__main__":
    # Basic instantiation of the database and running of the app.
    init_database()
    app.run()
