from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/orm_final.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))

Base = declarative_base()
Base.query = database_session.query_property()

def init_database():
    import temperature, user
    Base.metadata.create_all(bind=engine)

from user import User
from temperature import Temperature

class Manipulator:

    # Save

    def save_user(self, username=None, user_id=None, name=None, \
        email=None, mean_temperature=None):
        user = User(username, user_id, name, email, mean_temperature)
        database_session.add(user)
        database_session.commit()

    def save_temperature(self, sensor_id=None, mean_temperature=None):
        temperature = Temperature(sensor_id, mean_temperature)
        database_session.add(temperature)
        database_session.commit()

    # Query

    def get_user(self, user_id):
        return User.query.filter_by(user_id=user_id).first()

    def get_users_id(self, user_ids=None):
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

    def delete_users(self, user_id=None):
        users = [User.query.filter_by(user_id=user_id).first()] if user_id \
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
