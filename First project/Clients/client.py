import socket
import sys
import subprocess

while True:
    command = raw_input('\nEnter your command and I\'ll print the result (Type exit to leave): ')

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # address = str(sys.argv[1]) if len(sys.argv) > 1 else '0.0.0.0' # This is commented because it would be nice if you could pass the parameter too.
    address = subprocess.Popen('/sbin/ifconfig eth0 | grep "inet addr" | awk -F: \'{print $2}\' | awk \'{print $1}\'', stdout = subprocess.PIPE, shell = True).communicate()[0]
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
