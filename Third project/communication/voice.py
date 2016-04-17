# This will basically be a subclass of notification that will send command
# line arguments in order for the RBPi to talk.

from notification import Notification

class Voice(Notification):

    def __init__(self):
        super(Voice, self).__init__("say")
