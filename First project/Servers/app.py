import socket
import sys
import subprocess
import os

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

address = str(sys.argv[1]) if len(sys.argv) > 1 else '0.0.0.0'
server_address = (address, 10000)

print 'Python server listening on port %s' % server_address[1]

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)

while True:
    try:
        connection, client_address = sock.accept()
    except:
        print 'There was a problem accepting the incoming socket.'

    command = connection.recv(16)

    pid = os.fork()
    if pid == 0:
        sock.close()

        if command == "CPU":
            usage = subprocess.Popen('top -bn1 | grep "Cpu(s)" | sed "s/.*, *\([0-9.]*\)%* id.*/\1/" | awk \'{ print 100 - $1"%" }\'', stdout = subprocess.PIPE, shell = True)
            message = 'CPU: ' + str(usage.communicate()[0]).replace('\n', '')
        elif command == "MEM":
            totalMemory = float(subprocess.Popen('cat /proc/meminfo | grep MemTotal | awk \'{print $2}\'', stdout = subprocess.PIPE, shell = True).communicate()[0])
            freeMemory = float(subprocess.Popen('cat /proc/meminfo | grep MemFree | awk \'{print $2}\'', stdout = subprocess.PIPE, shell = True).communicate()[0])
            message = 'MEM: ' + str(int((totalMemory - freeMemory) * 100 / totalMemory)) + '%'
        elif command == "NET":
            message = str(subprocess.Popen('netstat -i', stdout = subprocess.PIPE, shell = True).communicate()[0])
        else:
            message = 'ERR: unknown command'

        connection.sendall(message)

        os._exit(0)

    connection.close()
