# All the prints that will appear in the app will be mainly logs, don't really
# want to put everywhere a '# logs', so this is a general rule accross the
# app.

# The app description will appear in the general README and the particular
# README in the folder this file is contained in.

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.voice import Voice
from communication.text import Text
from source.database.user import User
from source.database.temperature import Temperature

DATABASE = '/tmp/third.db'

if __name__ == '__main__':
    # Initialization of the main variables.

    nfc_sensor = NFCSensor()
    th_sensor = THSensor()
    user_model = User(DATABASE)
    temperature_model = Temperature(DATABASE)

    user_model.set_name('Ramon')
    user_model.set_nfc('1231323s')
    user_model.save()

    print user_model.get_objects()

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
