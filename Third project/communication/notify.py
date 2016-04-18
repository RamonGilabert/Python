from text import Text
from voice import Voice

class Notify:

    def __init__(self):
        print 'Configuration received'
        self.text = Text()
        self.voice = Voice()

    def broadcast(self, temperature, difference):
        for channel in [self.text, self.voice]:
            channel.broadcast(temperature, difference)
