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

# Helper methods

def _handle_request(id, endpoint, error_message, redirection, body, file_load, general):
    api_request = None
    flash_message = None

    if id is not None:
        api_request = urllib2.Request(api_url + '/' + endpoint + '/' \
        + str(id), body, headers)
        api_request.get_method = lambda: 'PATCH'
        flash_message = 'Your ' + error_message + ' has been saved'
    else:
        api_request = urllib2.Request(api_url + '/' + endpoint, body, headers)
        flash_message = 'Your ' + error_message + ' has been created'

    if api_request is not None:
        try:
            result = urllib2.urlopen(api_request)
            response = json.load(result)
            flash(flash_message)

            return redirect(url_for(redirection))
        except urllib2.HTTPError, error:
            errors = json.load(error)
            flash(errors['error'][0]) if 'error' in errors else flash(error)
        except:
            flash('There was an unknown error.')

    if file_load == 'new_sensor.html':
        return render_template(file_load, sensor=general)
    else:
        return render_template(file_load, user=general)

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

# We have to support POST instead of PATCH for the setup that we have in the
# HTML form that does not support PUT or PATCH as methods.
@app.route('/new_user', methods=['GET', 'POST'])
@app.route('/new_user/<string:id>', methods=['GET', 'POST'])
def new_user_view(id=None):
    general_user = None

    if id is not None:
        value = urllib2.urlopen(api_url + '/users/' + str(id))
        response = json.load(value)
        if 'data' in response:
            general_user = response['data'][0]

    if request.method == 'POST':
        user = json.dumps({
            'user_id': request.form['user_id'] if request.form['user_id'] else None,
            'username': request.form['username'] if request.form['username'] else None,
            'email': request.form['email'] if request.form['email'] else None,
            'name': request.form['name'] if request.form['name'] else None,
            'mean_temperature': float(request.form['mean_temperature'])
            if request.form['mean_temperature'] else None
        })

        return _handle_request(id, 'users', 'user', 'users_view', user, \
        'new_user.html', general_user)

    return render_template('new_user.html', user=general_user)

# Sensors

@app.route('/sensors')
def sensors_view():
    request = urllib2.urlopen(api_url + '/sensors')
    sensors = json.load(request)

    if 'data' in sensors:
        return render_template('sensors.html', sensors=sensors['data'])

@app.route('/new_sensor', methods=['GET', 'POST'])
@app.route('/new_sensor/<string:id>', methods=['GET', 'POST'])
def new_sensor_view(id=None):
    general_sensor = None

    if id is not None:
        value = urllib2.urlopen(api_url + '/sensors/' + str(id))
        response = json.load(value)

        if 'data' in response:
            general_sensor = response['data'][0]

    if request.method == 'POST':
        sensor = json.dumps({
            'sensor_id': request.form['sensor_id'] if request.form['sensor_id']
            else None,
            'mean_temperature': float(request.form['mean_temperature'])
            if request.form['mean_temperature'] else None
        })

        return _handle_request(id, 'sensors', 'sensor', 'sensors_view', sensor, \
        'new_sensor.html', general_sensor)

    return render_template('new_sensor.html', sensor=general_sensor)

if __name__ == "__main__":
    app.run(debug=True)
