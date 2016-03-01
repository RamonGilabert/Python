import unittest
import re, sys, socket

def send_parameter(ip,command):
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
        for cmd in ["MEM","CPU"]:
            result = send_parameter("localhost",cmd)
            t = re.match("^%s\:(\d*)%s$" % (cmd,"%"),result)
            self.assertEqual(True,t is not None)

    def test_error(self):
        result = send_parameter("localhost","wrong command")
        t = re.match("ERR: unknown command" ,result)
        self.assertEqual(True,t is not None)


def main():
    unittest.main()

if __name__ == '__main__':
    main()
