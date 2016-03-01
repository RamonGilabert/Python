import socket
import sys
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)

print 'Python server listening on port %s' % server_address[1]

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)

while True:
    command, address = sock.recvfrom(4096)

    if command:
        if command == "CPU":
            usage = subprocess.Popen('top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk \'{ print 100 - $1"%" }\'', stdout = subprocess.PIPE, shell = True)
            message = 'CPU: ' + str(usage.communicate()[0]).replace('\n', '')
        elif command == "MEM":
            totalMemory = float(subprocess.Popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'', stdout = subprocess.PIPE, shell = True).communicate()[0])
            freeMemory = float(subprocess.Popen('cat /proc/meminfo | grep MemFree | awk \'{print $2}\'', stdout = subprocess.PIPE, shell = True).communicate()[0])
            message = 'MEM: ' + str(int((totalMemory - freeMemory) * 100 / totalMemory)) + '%'
        else:
            message = 'ERR: unknown command'

        try:
            sock.sendto(message, ('localhost', int(sys.argv[1]))) \
            if len(sys.argv) > 1 else sock.sendto(message, address)
        except:
            print 'There was an error sending back the request'
