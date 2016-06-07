# This is the main implementation of the NFC Sensor.

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
        # Using the NFC library, this basically does a request to the reader
        # and checks the UID.
        (error, data) = self.reader.request()
        if not error:
            (error, UID) = self.reader.anticoll()
            if not error:
                return str(UID)
                self.reader.stop_crypto()

        return None
