import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print 'Attempting to connect to port %s' % server_address[1]
socket.connect(server_address)

try:
    socket.sendto('CPU', server_address)
    data, server = socket.recvfrom(4096)
    print data

    socket.sendto('MEM', server_address)
    data, server = socket.recvfrom(4096)
    print data

    socket.sendto('Wrong', server_address)
    data, server = socket.recvfrom(4096)
    print data

finally:
    print 'Closing socket'
    socket.close()
