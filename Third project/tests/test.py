import unittest
import re, sys, socket, imp

sys.path.append('./../')
from communication.text import Text

# This is the first test I've done in Python pretty much, so wanted to keep
# it as simple as possible. It just tests if the output is what it should
# be when we broadcast a Text.

def broadcast_temperature(temperature, difference):
    return Text().broadcast(temperature, difference)

class TestServer(unittest.TestCase):

    def test_notify(self):
        command = broadcast_temperature(25, 2)
        expected = 'The temperature is 25 degrees Celcius with ' + \
            'a difference of 2 degrees.'

        self.assertEqual(True, command == expected)

if __name__ == '__main__':
    unittest.main()
