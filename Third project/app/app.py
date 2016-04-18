# Main program.

import sys
import threading
import time

sys.path.append('./../')

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.notify import Notify
from source.database.user import User
from source.database.temperature import Temperature
from source.app import app

DATABASE = '/tmp/third.db'

class App(object):

    def __init__(self):
        # TODO: Parse the configuration file and start the program.
        self.nfc_sensor = NFCSensor()
        self.th_sensor = THSensor()
        self.notify = Notify()
        self.user_model = User(DATABASE)
        self.temperature_model = Temperature(DATABASE)

        self._prepare_threads()
        self._main_loop()

    # Private methods

    def _prepare_threads(self):
        self.app_thread = threading.Thread(target=self._run_web_app)
        self.app_thread.daemon = True
        self.app_thread.start()

    def _run_web_app(self):
        app.run()

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
