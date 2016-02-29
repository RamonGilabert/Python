import socket
import sys

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)
print >>sys.stderr, 'starting up on %s port %s' % server_address
socket.bind(server_address)

sock.listen(1)

while True:
    print >>sys.stderr, 'Waiting for a connection'
    connection, client_address = sock.accept()

    try:
        print >>sys.stderr, 'Connection from', client_address

        while True:
            data = connection.recv(16)
            print >>sys.stderr, 'Received "%s"' % data
            if data:
                print >>sys.stderr, 'Sending data back to the client'
                connection.sendall(data)
            else:
                print >>sys.stderr, 'No more data from', client_address
                break

    finally:
        connection.close()
