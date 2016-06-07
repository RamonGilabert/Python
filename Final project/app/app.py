# Main program.

import os
import sys
import threading
import time
import urllib2
import json
import random
import string

from ConfigParser import SafeConfigParser as Parser

sys.path.append('./../')

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.notify import Notify
from web_app.app import start as web_app_starter
from web_service.app import start as web_service_starter

api_url = 'http://127.0.0.1:8000'
headers = { 'Content-Type' : 'application/json' }

class App(object):

    def __init__(self):
        parser = Parser()
        parser.read('configuration.ini')

        # We instantiate the main variables of our program and the models with
        # the path of our DATABASE (that way we just have it in one place).

        self._channels = {'voice' : parser.getboolean('notifications', 'voice'),
            'text' : parser.getboolean('notifications', 'text')}
        self.nfc_sensor = NFCSensor()
        self.th_sensor = THSensor()
        self.notify = Notify(self._channels)
        self.serial_number = self._get_serial_number()
        self.current_sensor = None

        self._prepare_threads()

        time.sleep(1)

        self._prepare_sensor()
        self._main_loop()

    # Private methods

    def _handle_request(self, endpoint, body, id=None):

        # To generalize, those two variables will handle the api_request and the
        # message that will be sent after the request.
        api_request = None

        if id is not None:
            # We build the URL to do the request with the body and the headers.
            api_request = urllib2.Request(api_url + '/' + endpoint + '/' + \
            str(id), body, headers)

            # We specify that this needs to be a PATCH, this is because we have an
            # id, so the website has a user or a sensor that wants to patch.
            api_request.get_method = lambda: 'PATCH'
        else:
            api_request = urllib2.Request(api_url + '/' + endpoint, body, headers)
        if api_request is not None:
            # We have to try to get the response's error that the web service
            # will send to us.
            try:
                result = urllib2.urlopen(api_request)
                return json.load(result)
            except urllib2.HTTPError, error:
                errors = json.load(error)

                if 'error' in errors:
                    print errors['error'][0]

    def _prepare_sensor(self):
        print 'Preparing the sensors.'

        if os.system("ping -c 1 " + api_url) != 0:
            time.sleep(3)

        request = urllib2.urlopen(api_url + '/sensors')
        sensors = json.load(request)

        if 'data' in sensors:
            for sensor in sensors['data']:
                if sensor['sensor_id'] == self.serial_number:
                    self.current_sensor = sensor
                    break

            if self.current_sensor is None:
                sensor = json.dumps({
                    'sensor_id': self.serial_number,
                    'mean_temperature': None
                })

                response = self._handle_request('sensors', sensor)

                if 'data' in response:
                    self.current_sensor = response['data'][0]

    # Prepare threads is called to not cause a conflict between the main loop
    # and the server that will be running in the port 5000.
    def _prepare_threads(self):
        self.web_service_thread = threading.Thread(target=self._run_web_service)
        self.web_service_thread.daemon = True # To close the app when we CTRL+C.
        self.web_service_thread.start()

        self.app_thread = threading.Thread(target=self._run_web_app)
        self.app_thread.daemon = True # To close the app when we CTRL+C.
        self.app_thread.start()

    def _run_web_service(self):
        web_service_starter()

    def _run_web_app(self):
        web_app_starter()

    # We are going to basically save the information to the database and
    # perform all the changes that we've been asked we should do.
    def _perform_changes(self, data):
        initial_temperature = self._readings[0]
        final_temperature = self.th_sensor.get_data()
        difference = (final_temperature + initial_temperature) / 2

        sensor = json.dumps({
            'mean_temperature': difference
        })

        print self.current_sensor

        response = self._handle_request('sensors', sensor, \
        self.current_sensor['id'])

        if 'message' in response:
            self.current_sensor = response['message'][0]

        request = urllib2.urlopen(api_url + '/users')
        users = json.load(request)

        if 'data' in users:
            current_user = None
            for user in users['data']:
                if user['user_id'] == data:
                    current_user = user
                    break

            if current_user is None:
                user = json.dumps({
                    'user_id': data,
                    'username': ''.join(random.choice(string.ascii_lowercase + \
                    string.digits) for _ in range(20)),
                    'mean_temperature': difference
                })

                self._handle_request('users', user)
            else:
                user = json.dumps({
                    'mean_temperature': difference
                })

                self._handle_request('users', user, current_user['id'])

        self.notify.broadcast(initial_temperature, difference)

    def _main_loop(self):
        print 'Starting the main loop'

        self._initial_data = None
        self._readings = []

        try:
            while True:
                data = self.nfc_sensor.get_data()

                # It enters in the first if statement when a user reaches the
                # NFC, that is no readings yet, now we are going to save the
                # temperature and then save the initial data of the user, then
                # wait for the user to leave, which will be when the data is
                # None.

                if data is not None and len(self._readings) == 0:
                    self._initial_data = data
                    self._readings.append(self.th_sensor.get_data())
                elif data is None and len(self._readings) == 1:
                    self._perform_changes(self._initial_data)
                    self._initial_data = None
                    self._readings = []

                time.sleep(0.5)
        finally:
            print 'Closing the app.'

    def _get_serial_number(self):
        serial = "0000000000000000"
        try:
            file = open('/proc/cpuinfo', 'r')
            for line in file:
                if line[0:6]== 'Serial':
                    serial = line[10:26]
                    break
            file.close()
        except:
            serial = "ERROR000000000"

        return serial
