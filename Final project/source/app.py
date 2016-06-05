# Python web app.

import sqlite3
import urllib2
import json

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'

app = Flask(__name__)
app.config.from_object(__name__)

api_url = 'http://localhost:8000'

# Index

@app.route('/')
@app.route('/<string:message>')
def main_view(message=None):
    global general_message
    return render_template('index.html', message=message)

# Auth

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    message = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            message = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            message = 'Invalid password'
        else:
            session['logged_in'] = True
            message = 'You were logged in'
            return redirect(url_for('main_view', message=message))

    return render_template('login.html', message=message)

@app.route('/logout')
def logout():
    message = 'You were logged out'
    session.pop('logged_in', None)
    return redirect(url_for('main_view', message=message))

# Users

@app.route('/users')
def users_view():
    request = urllib2.urlopen(api_url + '/users')
    users = json.load(request)

    if 'data' in users:
        return render_template('users.html', users=users['data'])

@app.route('/users/<int:id>')
def user_view(id):
    return render_template('user.html', users=users)

@app.route('/new_user')
def new_user_view():
    return render_template('new_user.html')

# Sensors

@app.route('/sensors')
def sensors_view():
    request = urllib2.urlopen(api_url + '/sensors')
    sensors = json.load(request)

    if 'data' in sensors:
        return render_template('sensors.html', sensors=sensors['data'])

@app.route('/sensors/<int:id>')
def sensor_view(id):
    temperatures = connection.get_temperatures()
    return render_template('temperatures.html', temperatures=temperatures)

@app.route('/new_sensor')
def new_sensor_view():
    return render_template('new_sensor.html')

if __name__ == "__main__":
    app.run(debug=True)
