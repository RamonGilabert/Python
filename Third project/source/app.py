# Python web app.

import sqlite3
from connection import Connection
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

DATABASE = '/tmp/third.db'

app = Flask(__name__)
app.config.from_object(__name__)

connection = Connection(app)

def reload_temperatures():
    print 'Reload automatically.' # TODO: Implement this.
    # return redirect(url_for('temperatures_view'))

@app.before_request
def before_request():
    g.db = connection.connect_database()

@app.teardown_request
def teardown_request(exception):
    database = getattr(g, 'db', None)
    if database is not None:
        database.close()

def connect_database():
    return sqlite3.connect(app.config['DATABASE'])

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/temperatures')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

if __name__ == "__main__":
    connection.init_database()
