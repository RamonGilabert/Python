# All the prints that will appear in the app will be mainly logs, don't really
# want to put everywhere a '# logs', so this is a general rule accross the
# app.

# The app description will appear in the general README and the particular
# README in the folder this file is contained in.

from sensors.nfcsensor import NFCSensor
from sensors.thsensor import THSensor
from communication.notify import Notify
from source.database.user import User
from source.database.temperature import Temperature

DATABASE = '/tmp/third.db'

if __name__ == '__main__':
    # Initialization of the main variables.

    nfc_sensor = NFCSensor()
    th_sensor = THSensor()
    notify = Notify()
    user_model = User(DATABASE)
    temperature_model = Temperature(DATABASE)


    # try:
    #     while True:
    # finally:
