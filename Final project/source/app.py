# Python web app.

import sqlite3
from connection import Connection
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

@app.route('/')
def main_view():
    return render_template('index.html')

@app.route('/temperatures')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

if __name__ == "__main__":
    connection.init_database()
