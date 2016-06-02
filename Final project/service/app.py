from flask import Flask, jsonify, abort, make_response, request, Response
from database.connection import database_session, init_database, Manipulator

app = Flask(__name__)
manipulator = Manipulator()

# Errors

def check_errors(keys, request):
    error = []

    if not request:
        error.append('You should add a body in your request')
        return error

    for key in keys:
        if not key in request:
            error.append('The ' + key + ' cannot be undefined')

    return error

@app.errorhandler(404) # Not found error.
def not_found(error):
    return make_response(jsonify({ 'error': 'Not found' }), 404)

@app.errorhandler(400) # Bad request from the user.
def bad_request(error):
    return make_response(jsonify({ 'error': 'Bad request' }), 400)

# User requests

@app.route('/users', methods = ['GET', 'POST', 'DELETE'])
def api_users():
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id() })

    elif request.method == 'POST':
        error = check_errors(['username', 'user_id', 'email', 'name'], \
        request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        if manipulator.get_users_id([request.json['user_id']]) or \
        manipulator.get_users_username([request.json['username']]):
            error.append('Such user exists already')
            return make_response(jsonify({ 'error': error }), 400)

        user = {
            'username' : request.json['username'],
            'user_id': request.json['user_id'],
            'email': request.json['email'],
            'name': request.json['name']
        }

        manipulator.save_user(user['username'], user['user_id'], \
            user['name'], user['email'])

        return jsonify({ 'data': [user] }), 201

    elif request.method == 'DELETE':
        manipulator.delete_users()
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

@app.route('/users/<int:user_id>', methods = ['GET', 'PATCH', 'PUT', 'DELETE'])
def api_user(user_id):
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_users_id([user_id]) })

    elif request.method == 'PATCH':
        user = manipulator.get_user(user_id)

        if not user:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        if 'username' in request.json:
            if manipulator.get_users_username([request.json['username']]) \
            and user.username != request.json['username']:
                return make_response(jsonify({ 'error': \
                ['Such user exists already'] }), 400)
            else:
                user.username = request.json['username']

        # This is here as an optional thing. I don't think you should be able
        # to change the user_id.
        #
        # if 'user_id' in request.json:
        #     if manipulator.get_users_id([request.json['user_id']]) \
        #     and user.user_id != request.json['user_id']:
        #         return make_response(jsonify({ 'error': \
        #         ['Such user exists already'] }), 400)
        #     else:
        #         user.user_id = request.json['user_id']

        if 'email' in request.json:
            user.email = request.json['email']

        if 'name' in request.json:
            user.name = request.json['name']

        if 'mean_temperature' in request.json:
            user.mean_temperature = request.json['mean_temperature']

        database_session.commit()

        return jsonify({ 'message': [user.serialize()] }), 200

    elif request.method == 'PUT':
        error = check_errors(['username'], request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        user = manipulator.get_user(user_id)

        if not user:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        if manipulator.get_users_username([request.json['username']]) \
        and user.username != request.json['username']:
            return make_response(jsonify({ 'error': \
            ['Such user exists already'] }), 400)
        else:
            user.username = request.json['username']

        user.email = request.json['email'] if 'email' in request.json else None
        user.name = request.json['name'] if 'name' in request.json else None
        user.mean_temperature = request.json['mean_temperature'] \
        if 'mean_temperature' in request.json else None

        database_session.commit()

        return jsonify({ 'message': [user.serialize()] }), 200

    elif request.method == 'DELETE':
        manipulator.delete_users(user_id)
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

# Sensor requests

@app.route('/sensors', methods = ['GET', 'POST', 'DELETE'])
def api_sensors():
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_temperatures_id() })

    elif request.method == 'POST':
        error = check_errors(['sensor_id'], request.json)

        if error:
            return make_response(jsonify({ 'error': error }), 400)

        if manipulator.get_temperatures_id([request.json['sensor_id']]):
            error.append('Such user exists already')
            return make_response(jsonify({ 'error': error }), 400)

        sensor = {
            'sensor_id' : request.json['sensor_id'],
            'mean_temperature': request.json['mean_temperature']
        }

        manipulator.save_temperature(sensor['sensor_id'], sensor['mean_temperature'])

        return jsonify({ 'data': [sensor] }), 201

    elif request.method == 'DELETE':
        manipulator.delete_temperatures()
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

@app.route('/sensors/<int:sensor_id>', methods = ['GET', 'PATCH', 'PUT', 'DELETE'])
def api_sensor(sensor_id):
    if request.method == 'GET':
        return jsonify({ 'data' : manipulator.get_temperature(sensor_id) })

    elif request.method == 'PATCH':
        sensor = manipulator.get_temperature(sensor_id)

        if not sensor:
            return make_response(jsonify({ 'error': ['No such sensor'] }), 400)

        if 'mean_temperature' in request.json:
            sensor.mean_temperature = request.json['mean_temperature']

        database_session.commit()

        return jsonify({ 'message': [sensor.serialize()] }), 200

    elif request.method == 'PUT':
        if check_errors([], request.json):
            return make_response(jsonify({ 'error': error }), 400)

        sensor = manipulator.get_temperature(sensor_id)

        if not sensor:
            return make_response(jsonify({ 'error': ['No such user'] }), 400)

        sensor.mean_temperature = request.json['mean_temperature'] if \
        'mean_temperature' in request.json else None

        database_session.commit()

        return jsonify({ 'message': [sensor.serialize()] }), 200

    elif request.method == 'DELETE':
        manipulator.delete_temperatures(sensor_id)
        return jsonify({ 'message': ['Your data is gone'] }), 200

    else:
        abort(404)

if __name__ == '__main__':
    init_database()
    app.run(debug=True)
