import socket
import sys
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# address = str(sys.argv[1]) if len(sys.argv) > 1 else '0.0.0.0' # I think this is a nice thing to have in case you want to send the address yourself.
address = subprocess.Popen('/sbin/ifconfig eth0 | grep "inet addr" | awk -F: \'{print $2}\' | awk \'{print $1}\'', stdout = subprocess.PIPE, shell = True).communicate()[0]
server_address = (address, 10000)

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
