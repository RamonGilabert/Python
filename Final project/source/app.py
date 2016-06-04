# Python web app.

import sqlite3
from connection import Connection
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash

app = Flask(__name__)
app.config.from_object(__name__)

# Index

@app.route('/')
def main_view():
    return render_template('index.html')

# Login

@app.route('/login')
def main_view():
    return render_template('index.html')

# Users

@app.route('/users')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/users/<int:id>')
def temperatures_view(id):
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/new_user')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

# Sensors

@app.route('/sensors')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/sensors/<int:id>')
def temperatures_view(id):
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/new_sensor')
def temperatures_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)


if __name__ == "__main__":
    connection.init_database()
