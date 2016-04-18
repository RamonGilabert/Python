# This is the main notification class. This is just to show a rough estimate of
# what the subclasses of it can be. Basically a header file.

import os

class Notification(object):

    def __init__(self, command):
        self.command = command

    def broadcast(self, temperature):
        message = 'The temperature is ' + str(temperature) + ' degrees Celcius \
            with a difference of ' + str(difference) + ' degrees.'
        os.system(self.command + ' ' + message)

        return message
