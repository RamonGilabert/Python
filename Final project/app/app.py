# Main program.

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
from web_app.app import app
from web_service.app import app as web_service_app

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

    def _prepare_sensor(self):
        print 'Preparing the sensors.'

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

                api_request = urllib2.Request(api_url + '/sensors', sensor, \
                headers)

                try:
                    result = urllib2.urlopen(api_request)
                    sensor = json.load(result)

                    if 'data' in sensor:
                        self.current_sensor = sensor['data'][0]
                except urllib2.HTTPError, error:
                    print 'There was an error processing the request.'

    # Prepare threads is called to not cause a conflict between the main loop
    # and the server that will be running in the port 5000.
    def _prepare_threads(self):
        self.app_thread = threading.Thread(target=self._run_web_app)
        self.app_thread.daemon = True # To close the app when we CTRL+C.
        self.app_thread.start()

        self.web_service_thread = threading.Thread(target=self._run_web_service)
        self.web_service_thread.daemon = True # To close the app when we CTRL+C.
        self.web_service_thread.start()

    def _run_web_app(self):
        app.run(port=7000)

    def _run_web_service(self):
        web_service_app.run(port=8000)

    # We are going to basically save the information to the database and
    # perform all the changes that we've been asked we should do.
    def _perform_changes(self, data):
        initial_temperature = self._readings[0]
        final_temperature = self.th_sensor.get_data()
        difference = (final_temperature + initial_temperature) / 2

        sensor = json.dumps({
            'mean_temperature': difference
        })

        api_request = urllib2.Request(api_url + '/sensors/' + \
        str(self.current_sensor['id']), sensor, headers)
        api_request.get_method = lambda: 'PATCH'

        try:
            result = urllib2.urlopen(api_request)
            sensor = json.load(result)

            if 'message' in sensor:
                self.current_sensor = sensor['message'][0]
        except urllib2.HTTPError, error:
            print 'There was an error processing the request.'

        ######################################################

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

                api_request = urllib2.Request(api_url + '/users', user, headers)

                try:
                    result = urllib2.urlopen(api_request)
                except urllib2.HTTPError, error:
                    print 'There was an error processing the request.'
            else:
                user = json.dumps({
                    'mean_temperature': difference
                })

                api_request = urllib2.Request(api_url + '/users/' + \
                str(current_user['id']), user, headers)
                api_request.get_method = lambda: 'PATCH'

                try:
                    result = urllib2.urlopen(api_request)
                except urllib2.HTTPError, error:
                    print 'There was an error processing the request.'

        ######################################################

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
