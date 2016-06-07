# This is the main notification class. This is just to show a rough estimate of
# what the subclasses of it can be. Basically a header file.

import os

class Notification(object):

    def __init__(self, command):
        self.command = command

    # To have it just in one place, we configure the message here so we just
    # have to change it here and everything looks tidier in the app file.
    def broadcast(self, temperature, difference):
        message = 'The temperature is ' + str(temperature) + ' degrees ' + \
            'Celcius with a mean temperature of ' + str(difference) + ' degrees.'
        os.system(self.command + ' ' + message)

        return message
