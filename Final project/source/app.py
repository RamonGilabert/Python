# Python web app.

import sqlite3
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
def login_view():
    return render_template('index.html')

# Users

@app.route('/users')
def users_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/users/<int:id>')
def user_view(id):
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/new_user')
def new_user_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

# Sensors

@app.route('/sensors')
def sensors_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/sensors/<int:id>')
def sensor_view(id):
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/new_sensor')
def new_sensor_view():
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

if __name__ == "__main__":
    app.run(debug=True)
