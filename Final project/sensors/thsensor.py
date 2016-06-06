# This will be the main implementation of the DHT11 Sensor.

# IMPORTANT: FOR NOT THIS WILL BE MOCKED, SO THE COMMENTED CODE BELOW WILL
# BE THE ONE THAT WILL BE USED.

from sensor import Sensor

import RPi.GPIO as GPIO
import Adafruit_DHT as DHT

class THSensor(Sensor):

    def __init__(self):
        print 'Sensor instantiated.'
        self._temperature = None

    def get_data(self):
        humidity, self._temperature = DHT.read_retry(DHT.DHT11, 22)
        return self._temperature

    def get_cumulative(self):
        initial_temperature = self._temperature
        final_temperature = self.get_data()

        return final_temperature - initial_temperature

    def reset_cumulative(self):
        self._temperature = None
