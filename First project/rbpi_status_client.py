import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
print 'Attempting to connect to port %s' % server_address[1]

try:
    while True:
        command = raw_input('\nEnter your command and I\'ll print the result (Type exit to leave): ')

        if command == 'exit':
            break
        else:
            sock.sendto(command, server_address)
            data, server = sock.recvfrom(4096)
            print '\n' + data
finally:
    print '\nClosing socket\n'
    sock.close()
