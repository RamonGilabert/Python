import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print 'Python server listening on port %s' % server_address[1]

socket.bind(server_address)
socket.listen(1)

while True:
    connection, client_address = socket.accept()

    try:
        print 'There\'s a new connection from:', client_address

        while True:
            command = connection.recv(16)
            print command
            if command == "CPU":
                message = 'CPU: 123'
            elif command == "MEM":
                message = 'MEM: 123'
            else:
                message = 'There was an error with your request.'

            if len(sys.argv) > 1:
                address = ('localhost', int(sys.argv[1]))
                try:
                    connection.sendto(message, address)
                except:
                    break
            else:
                try:
                    connection.sendall(message)
                except:
                    break
    finally:
        connection.close()
