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
headers = { 'Content-Type' : 'application/json' }

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

@app.route('/new_user', methods=['GET', 'POST'])
@app.route('/new_user/<string:id>', methods=['GET', 'PATCH'])
def new_user_view(id=None):
    general_user = None
    if request.method == 'GET':
        if id is not None:
            value = urllib2.urlopen(api_url + '/users/' + str(id))
            response = json.load(value)
            if 'data' in response:
                general_user = response['data'][0]
    elif request.method == 'POST' or request.method == 'PATCH':
        user = json.dumps({
            'user_id': request.form['user_id'] if request.form['user_id'] else None,
            'username': request.form['username'] if request.form['username'] else None,
            'email': request.form['email'] if request.form['email'] else None,
            'name': request.form['name'] if request.form['name'] else None,
            'mean_temperature': float(request.form['mean_temperature'])
            if request.form['mean_temperature'] else None
        })

        if request.method == 'POST':
            value = urllib2.Request(api_url + '/users', user, headers)

            try:
                result = urllib2.urlopen(value)
                response = json.load(result)

                user = response['data'][0]
                flash('Your user has been created')
                return redirect(url_for('users_view'))
            except urllib2.HTTPError, error:
                flash(error)
        else:
            print 'Configure the PATCH.'

    return render_template('new_user.html', user=general_user)

# Sensors

@app.route('/sensors')
def sensors_view():
    request = urllib2.urlopen(api_url + '/sensors')
    sensors = json.load(request)

    if 'data' in sensors:
        return render_template('sensors.html', sensors=sensors['data'])

@app.route('/new_sensor', methods=['GET', 'POST'])
@app.route('/new_sensor/<string:id>', methods=['GET', 'PATCH'])
def new_sensor_view(id=None):
    sensor = None
    if request.method == 'GET':
        if id is not None:
            value = urllib2.urlopen(api_url + '/sensors/' + str(id))
            data = json.load(value)
            sensor = data['data'][0]
    elif request.method == 'POST' or request.method == 'PATCH':
        sensor = json.dumps({
            'sensor_id': request.form['sensor_id'] if request.form['sensor_id']
            else None,
            'mean_temperature': float(request.form['mean_temperature'])
            if request.form['mean_temperature'] else None
        })

        if request.method == 'POST':
            value = urllib2.Request(api_url + '/users', user, headers)
            result = urllib2.urlopen(value)
            response = json.load(result)

            if 'data' in response:
                user = response['data'][0]
                flash('Your user has been created')
                return redirect(url_for('users_view'))
            elif 'error' in response:
                flash(response['error'][0])
        else:
            print 'Configure the PATCH.'

    return render_template('new_sensor.html', sensor=sensor)

if __name__ == "__main__":
    app.run(debug=True)
