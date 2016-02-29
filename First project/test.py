import unittest
import re, sys, socket

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
        for command in ["MEM","CPU"]:
            result = send_parameter("localhost", command)
            t = re.match("^%s\:(\d*)%s$" % (command, "%"),result)
            self.assertEqual(True, t is not None)

    def test_error(self):
        result = send_parameter("localhost", "Wrong")
        t = re.match("There was an error with your request.", result)
        self.assertEqual(True, t is not None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
