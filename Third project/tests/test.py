import unittest
import re, sys, socket, imp

sys.path.append('./../')
from communication.text import Text

def broadcast_temperature(temperature):
    text = Text()

    return text.broadcast(temperature)

class TestServer(unittest.TestCase):

    def test_notify(self):
        command = broadcast_temperature(25)
        expected = 'The temperature is 25 degrees Celcius.'

        self.assertEqual(True, command == expected)

if __name__ == '__main__':
    unittest.main()
