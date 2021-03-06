# Main program.

import sys
import threading
import time

from ConfigParser import SafeConfigParser as Parser

sys.path.append('./../')

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.notify import Notify
from source.database.user import User
from source.database.temperature import Temperature
from source.app import app

class App(object):

    def __init__(self):
        parser = Parser()
        parser.read('configuration.ini')

        # We instantiate the main variables of our program and the models with
        # the path of our DATABASE (that way we just have it in one place).

        self._database = parser.get('database', 'path')
        self._channels = {'voice' : parser.getboolean('notifications', 'voice'),
            'text' : parser.getboolean('notifications', 'text')}
        self.nfc_sensor = NFCSensor()
        self.th_sensor = THSensor()
        self.notify = Notify(self._channels)
        self.user_model = User(self._database)
        self.temperature_model = Temperature(self._database)

        self._prepare_threads()
        self._main_loop()

    # Private methods

    # Prepare threads is called to not cause a conflict between the main loop
    # and the server that will be running in the port 5000.
    def _prepare_threads(self):
        self.app_thread = threading.Thread(target=self._run_web_app)
        self.app_thread.daemon = True # To close the app when we CTRL+C.
        self.app_thread.start()

    def _run_web_app(self):
        app.run()

    # We are going to basically save the information to the database and
    # perform all the changes that we've been asked we should do.
    def _perform_changes(self):
        initial_temperature = self._readings[0]
        final_temperature = self.th_sensor.get_data()
        difference = final_temperature - initial_temperature
        date = time.strftime('%d.%m.%Y at %H:%M')

        self.user_model.add(self._initial_data['name'], \
            self._initial_data['nfc'])
        self.temperature_model.add(initial_temperature, date, \
            difference, self._initial_data['nfc'])
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
                    self._perform_changes()
                    self._initial_data = None
                    self._readings = []

                time.sleep(2) # TODO: Delete this when implementing.
        finally:
            print 'Closing the app.'
