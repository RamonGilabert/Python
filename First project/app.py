import socket
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print 'Python server listening on port %s' % server_address[1]

sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:
        print 'There\'s a new connection from:', client_address

        while True:
            command = connection.recv(16)

            if command == "CPU":
                message = 'CPU: 123%'
            elif command == "MEM":
                message = 'MEM: 123%'
            else:
                message = 'ERR: unknown command'

            try:
                connection.sendto(message, ('localhost', int(sys.argv[1]))) \
                if len(sys.argv) > 1 else connection.sendall(message)
            except:
                break
    finally:
        connection.close()
