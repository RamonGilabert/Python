import socket
import sys

while True:
    command = raw_input('\nEnter your command and I\'ll print the result (Type exit to leave): ')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    address = str(sys.argv[1]) if len(sys.argv) > 1 else '0.0.0.0'
    server_address = (address, 10000)

    sock.connect(server_address)

    if command == 'exit':
        sock.close()
        break
    else:
        sock.sendto(command, server_address)
        data, server = sock.recvfrom(4096)
        print '\n' + data

    sock.close()
