# This will basically be a subclass of notification that will send command
# line arguments in order for the RBPi to talk.

from notification import Notification

class Text(Notification):

    def __init__(self):
        super(Text, self).__init__("echo")
