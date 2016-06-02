from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from user import User
from temperature import Temperature

engine = create_engine('sqlite:////tmp/orm_final.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
                                               autoflush=False,
                                               bind=engine))

Base = declarative_base()
Base.query = database_session.query_property()

def init_database():
    import temperature, user
    Base.metadata.create_all(bind=engine)

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

def get_users(self, usernames):
    users = []
    for username in usernames:
        users.extend(User.query.filter_by(username=username).first())

    return users


def get_temperatures(self, sensor_ids):
    temperatures = []
    for id in sensor_ids:
        temperatures.extend(Temperature.query.filter_by(sensor_id=id).first())

    return temperatures

# Delete

def delete_users(self):
    # TODO: Add the delete of the users.
    database_session.delete()
    database_session.commit()

def delete_temperatures(self):
    # TODO: Add the delete of the temperatures.
    database_session.delete()
    database_session.commit()
