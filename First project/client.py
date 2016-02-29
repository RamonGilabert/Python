import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print 'Attempting to connect to port %s' % server_address[1]
socket.connect(server_address)

try:
    while True:
        command = raw_input('\nEnter your command and I\'ll print the result (Type exit to leave): ')

        if command == 'exit':
            break
        else:
            socket.sendto(command, server_address)
            data, server = socket.recvfrom(4096)
            print data

finally:
    print '\nClosing socket\n'
    socket.close()
