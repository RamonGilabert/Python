from text import Text
from voice import Voice

class Notify:

    def __init__(self, channels):
        print 'Configuration received'

        self._channels = []

        # Gets the configuration and based on that creates one instance,
        # another or both.
        if channels['text']:
            self.text = Text()
            self._channels.append(self.text)

        if channels['voice']:
            self.voice = Voice()
            self._channels.append(self.voice)

    def broadcast(self, temperature, difference):
        for channel in self._channels:
            channel.broadcast(temperature, difference)
