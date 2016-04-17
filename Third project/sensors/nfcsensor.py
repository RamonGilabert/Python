# This will be the main implementation of the NFC Sensor.

# IMPORTANT: FOR NOW EVERYTHING IS MOCKED, THIS WILL CHANGE WHEN HAVING
# THE ACTUAL SENSOR WITH THE ACTUAL DATA.

from sensor import Sensor
import random

class NFCSensor(Sensor):

    def __init__(self):
        print "NFC Sensor instantiated."

    def setup(self):
        print "Preparing the sensor."
        # TODO: Here we'll connect the sensor and prepare it. Since I haven't
        # worked with an NFC sensor, I don't really know the setup that it
        # needs.

    def get_data(self):
        # TODO: Remove the mocked data.
        value = random.randint(0, 3)
        return { 'name' : 'Ramon', 'nfc' : 'safqwr21oi3asd' } \
            if value == 0 else None
