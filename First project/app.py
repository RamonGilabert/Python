import socket
import sys
import subprocess

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server_address = ('localhost', 10000)

print 'Python server listening on port %s' % server_address[1]

sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sock.bind(server_address)
sock.listen(1)

while True:
    connection, client_address = sock.accept()

    try:
        print 'There\'s a new connection from:', client_address

        while True:
            command = connection.recv(16)

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
                connection.sendto(message, ('localhost', int(sys.argv[1]))) \
                if len(sys.argv) > 1 else connection.sendall(message)
            except:
                break
    finally:
        connection.close()
