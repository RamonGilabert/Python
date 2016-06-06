# This will be the main implementation of the NFC Sensor.

# IMPORTANT: FOR NOW EVERYTHING IS MOCKED, THIS WILL CHANGE WHEN HAVING
# THE ACTUAL SENSOR WITH THE ACTUAL DATA.

from sensor import Sensor
from libraries.NFC import RFID

import signal
import time

class NFCSensor(Sensor):

    def __init__(self):
        print 'NFC Sensor instantiated.'
        self.reader = RFID.RFID()

    def setup(self):
        print 'Preparing the NFC sensor.'

    def get_data(self):
        (error, data) = self.reader.request()
        if not error:
            (error, UID) = self.reader.anticoll()
            if not error:
                print 'UID: ' + str(UID)
                if not self.reader.select_tag(UID):
                    if not self.reader.card_auth(self.reader.auth_a, 10, \
                    [0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF], UID):
                      print 'Reading block 10: ' + str(self.reader.read(10))
                      self.reader.stop_crypto()

        # { 'name' : 'Ramon', 'nfc' : 'safqwr21oi3asd' }
