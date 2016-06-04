from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Initialization of the engine with the address of the database.
# initializing also the base and everything required for the database
# to run.

engine = create_engine('sqlite:////tmp/orm_final.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))

Base = declarative_base()
Base.query = database_session.query_property()

def init_database():
    import temperature, user
    Base.metadata.create_all(bind=engine)

# A Sensor is saved in the database as Temperature, to just display that
# is a temperature sensor, just naming.

from user import User
from temperature import Temperature

# Manipulator is the one that will talk to the database making the web service
# backend, or anything that uses it agnostic to it.
class Manipulator:

    # Save

    # In the save we don't check for errors, errors needs to be already checked
    # since the method name is basically save something, that save needs to be
    # correct with an error shown already if any.

    def save_user(self, username=None, user_id=None, name=None, \
        email=None, mean_temperature=None):
        # Create a user and save it.
        user = User(username, user_id, name, email, mean_temperature)
        database_session.add(user)
        database_session.commit()

    def save_temperature(self, sensor_id=None, mean_temperature=None):
        # Create a temperature and save it.
        temperature = Temperature(sensor_id, mean_temperature)
        database_session.add(temperature)
        database_session.commit()

    # Query

    # Similar methods but with a different query in the database, that makes it
    # is the reason why is a bit hard to make it generic. It will comment the
    # first one and that's it, understanding that all work the same way.

    def get_user(self, id):
        return User.query.filter_by(id=id).first()

    def get_users_id(self, ids=None):
        # If not array then it will return all of them serialized.
        if not ids:
            return [user.serialize() for user in User.query.all()]

        # If there are ids, it will iterate through all of them and
        # save them into the array.
        users = []
        for id in ids:
            user = User.query.filter_by(id=id).first()
            if user is not None:
                users.append(user.serialize())

        return users

    def get_users_user_id(self, user_ids=None):
        if not user_ids:
            return [user.serialize() for user in User.query.all()]

        users = []
        for id in user_ids:
            user = User.query.filter_by(user_id=id).first()
            if user is not None:
                users.append(user.serialize())

        return users

    def get_users_username(self, usernames=None):
        if not usernames:
            return [user.serialize() for user in User.query.all()]

        users = []
        for username in usernames:
            user = User.query.filter_by(username=username).first()
            if user is not None:
                users.append(user.serialize())

        return users

    def get_temperature(self, id):
        return Temperature.query.filter_by(id=id).first()

    def get_temperatures_sensors(self, sensor_ids=None):
        if sensor_ids is None:
            return [temperature.serialize() for temperature in Temperature.query.all()]

        temperatures = []
        for id in sensor_ids:
            temperature = Temperature.query.filter_by(sensor_id=id).first()
            if temperature is not None:
                temperatures.append(temperature.serialize())

        return temperatures

    def get_temperatures_id(self, ids=None):
        if ids is None:
            return [temperature.serialize() for temperature in Temperature.query.all()]

        temperatures = []
        for id in ids:
            temperature = Temperature.query.filter_by(id=id).first()
            if temperature is not None:
                temperatures.append(temperature.serialize())

        return temperatures

    # Delete

    # Delete calls a private method that will do the deletion in the
    # database_session. It first gets all the users or temperatures
    # and basically deletes them.
    
    def delete_users(self, id=None):
        users = [User.query.filter_by(id=id).first()] if id \
        else User.query.all()
        self._delete_object(users)

    def delete_temperatures(self, id=None):
        temperatures = [Temperature.query.filter_by(id=id).first()] \
        if id else Temperature.query.all()
        self._delete_object(temperatures)

    def _delete_object(self, objects):
        if not objects:
            return

        for object in objects:
            if object:
                database_session.delete(object)

        database_session.commit()

    # Database session

    def initialize(self):
        init_database()

    def commit(self):
        database_session.commit()
