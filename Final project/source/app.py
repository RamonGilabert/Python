# Python web app.

import sqlite3
import urllib2
import json

from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash, jsonify

SECRET_KEY = 'NbrIvaX9a78KxVlTFs9YmVqIgg7uCzAG'
USERNAME = 'admin'
PASSWORD = '123'

# We instantiate the app with the main configuration.
app = Flask(__name__)
app.config.from_object(__name__)

# Constants for the server, in this case localhost in the 8000 port and
# the headers that we'll use for the POST and PATCH requests.
api_url = 'http://localhost:8000'
headers = { 'Content-Type' : 'application/json' }

# Helper methods

def _fetch_parameter(id, endpoint):
    if id is not None:
        value = urllib2.urlopen(api_url + '/' + endpoint + '/' + str(id))
        response = json.load(value)

        if 'data' in response:
            return response['data'][0]

    return None

# This method handles the POST or PATCH requests of the new users or edit users.
def _handle_request(id, endpoint, error_message,
redirection, body, file_load, general):

    # To generalize, those two variables will handle the api_request and the
    # message that will be sent after the request.
    api_request = None
    flash_message = None

    if id is not None:
        # We build the URL to do the request with the body and the headers.
        api_request = urllib2.Request(api_url + '/' + endpoint + '/' \
        + str(id), body, headers)

        # We specify that this needs to be a PATCH, this is because we have an
        # id, so the website has a user or a sensor that wants to patch.
        api_request.get_method = lambda: 'PATCH'

        # The general flash message that we'll send.
        flash_message = 'Your ' + error_message + ' has been saved'
    else:
        api_request = urllib2.Request(api_url + '/' + endpoint, body, headers)
        flash_message = 'Your ' + error_message + ' has been created'

    if api_request is not None:
        # We have to try to get the response's error that the web service
        # will send to us.
        try:
            result = urllib2.urlopen(api_request)
            response = json.load(result)
            flash(flash_message)

            return redirect(url_for(redirection))
        except urllib2.HTTPError, error:
            errors = json.load(error)
            # We unwrap the error if any and show it with a flash, if not,
            # we show the general error that appears, for instance: BAD REQUEST.
            flash(errors['error'][0]) if 'error' in errors else flash(error)
        except:
            flash('There was an unknown error.')

    # The difficulty to make this generic since it has one argument in it makes
    # it a bit 'ugly' in a sense, but it works for now, we could implement
    # promises etc. to make it work nicer.
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
    # Check if the username, etc. match with the configuration that we have.
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
    # Normal GET request.
    request = urllib2.urlopen(api_url + '/users')

    # We use the JSON library in order to load what the request contains.
    users = json.load(request)

    if 'data' in users:
        return render_template('users.html', users=users['data'])

# We have to support POST instead of PATCH for the setup that we have in the
# HTML form that does not support PUT or PATCH as methods.
@app.route('/new_user', methods=['GET', 'POST'])
@app.route('/new_user/<string:id>', methods=['GET', 'POST'])
def new_user_view(id=None):
    # If there is an id, there should be a user, this fetches such user and
    # saves it into a property that will be used later.
    general_user = _fetch_parameter(id, 'users')

    # We do a security check in order to append in the object None or the actual
    # value. If this exist, we just save it.
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
    general_sensor = _fetch_parameter(id, 'sensors')

    # This is basically the same as the user but tailored to the sensor,
    # what could be generic is generic in the private function that we've
    # commented before, the other part is the part of creating the actual
    # object, which cannot be generalized.

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
