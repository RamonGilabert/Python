# All the prints that will appear in the app will be mainly logs, don't really
# want to put everywhere a '# logs', so this is a general rule accross the
# app.

# The app description will appear in the general README and the particular
# README in the folder this file is contained in.

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.voice import voice
from communication.text import text

if __name__ == '__main__':
    nfc = NFCSensor()
    temperature = THSensor()

    # try:
    #     while True:
    #         command = raw_input('\nEnter your command and I\'ll print the result (Type exit to leave): ')
    #
    #         if command == 'exit':
    #             break
    #         else:
    #             sock.sendto(command, server_address)
    #             data, server = sock.recvfrom(4096)
    #             print '\n' + data
    # finally:
    #     print '\nClosing socket\n'
    #     sock.close()
