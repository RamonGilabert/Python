from flask import Flask, jsonify, abort, make_response, request, Response
from database.connection import database_session, init_database, Manipulator

app = Flask(__name__)

# Errors

@app.errorhandler(404) # Not found error.
def not_found(error):
    return make_response(jsonify( {'error': 'Not found'} ), 404)

@app.errorhandler(400) # Bad request from the user.
def bad_request(error):
    return make_response(jsonify( {'error': 'Bad request'} ), 400)

# User requests

@app.route('/users', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_users():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

@app.route('/users/<int:user_id>', methods = ['GET', 'POST', 'PATCH', \
    'PUT', 'DELETE'])
def api_user():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

# Sensor requests

@app.route('/sensors', methods = ['GET', 'POST', 'PATCH', 'PUT', 'DELETE'])
def api_sensors():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

@app.route('/sensors/<int:sensor_id>', methods = ['GET', 'POST', 'PATCH', \
    'PUT', 'DELETE'])
def api_sensor():
    if request.method == 'GET':
        return "ECHO: GET\n"

    elif request.method == 'POST':
        return "ECHO: POST\n"

    elif request.method == 'PATCH':
        return "ECHO: PACTH\n"

    elif request.method == 'PUT':
        return "ECHO: PUT\n"

    elif request.method == 'DELETE':
        return "ECHO: DELETE"

    else:
        abort(404)

if __name__ == '__main__':
    init_database()
    app.run()
