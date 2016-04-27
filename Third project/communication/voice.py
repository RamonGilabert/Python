# This will basically be a subclass of notification that will send command
# line arguments in order for the RBPi to talk.

import pyttsx as Engine
import threading

from notification import Notification

class Voice(Notification):

    def __init__(self):
        print 'Voice command initiated.'
        self.engine_thread = None

    # We are going to put here a custom implementation for the voice, different
    # than the parent's implementation, so it overrides it.
    def broadcast(self, temperature, difference):
        self._message = 'The temperature is ' + str(temperature) + ' degrees ' + \
            'Celcius with a difference of ' + str(difference) + ' degrees.'

        self._prepare_engine()

        return self._message

    def _prepare_threads(self):
        self.engine_thread = threading.Thread(target=self._prepare_engine)
        self.engine_thread.daemon = True # To close the app when we CTRL+C.
        self.engine_thread.start()

    def _prepare_engine(self):
        def onEnd(name, completed):
            self.engine.endLoop()
            self.engine.stop()

        self.engine = Engine.init()
        self.engine.connect('finished-utterance', onEnd)
        self.engine.say(self._message)
        self.engine.startLoop()
