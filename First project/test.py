import unittest
import socket
import re, sys

def send_parameter(ip, command):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    server_address = (ip, 10000)
    message = command

    try:
        sent = sock.sendto(message, server_address)
        data, server = sock.recvfrom(4096)
        return data
    finally:
        sock.close()

class TestServer(unittest.TestCase):

    def test_mem_and_cpu(self):
        for command in ["CPU", "MEM"]:
            result = send_parameter('localhost', command)
            t = re.match("^%s\: (\d*)%s$" % (command, "%"), result)
            self.assertEqual(True, t is not None)

    def test_error(self):
        result = send_parameter('localhost', "Wrong")
        t = re.match("ERR: unknown command", result)
        self.assertEqual(True, t is not None)

if __name__ == '__main__':
    unittest.main()
