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
def main_view():
    return render_template('index.html')

# Auth

@app.route('/login', methods=['GET', 'POST'])
def login_view():
    message = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            flash('Invalid username')
        elif request.form['password'] != app.config['PASSWORD']:
            flash('Invalid password')
        else:
            session['logged_in'] = True
            flash('You are now logged in')
            return redirect(url_for('main_view'))

    return render_template('login.html')

@app.route('/logout')
def logout():
    flash('You are now logged out')
    session.pop('logged_in', None)
    return redirect(url_for('main_view'))

# Users

@app.route('/users')
def users_view():
    request = urllib2.urlopen(api_url + '/users')
    users = json.load(request)

    if 'data' in users:
        return render_template('users.html', users=users['data'])

@app.route('/new_user')
@app.route('/new_user/<int:id>')
def new_user_view(id=None):
    user = {
        "user_id": 21,
        "username": 'Monrachu',
        "name": None,
        "email": None,
        "mean_temperature": None
    }

    return render_template('new_user.html', user=user)

# Sensors

@app.route('/sensors')
def sensors_view():
    request = urllib2.urlopen(api_url + '/sensors')
    sensors = json.load(request)

    if 'data' in sensors:
        return render_template('sensors.html', sensors=sensors['data'])

@app.route('/new_sensor')
@app.route('/new_sensor/<int:id>')
def new_sensor_view(id=None):
    sensor = {
        "sensor_id": 21,
        "mean_temperature": None
    }
    return render_template('new_sensor.html', sensor=sensor)

if __name__ == "__main__":
    app.run(debug=True)
