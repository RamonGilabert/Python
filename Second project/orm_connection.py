from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# We declare the engine, which needs the url of the database.
engine = create_engine('sqlite:////tmp/orm_users.db', convert_unicode=True)

# The database_session is the one that will talk to the persistency layer.
database_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False, bind=engine))

# We declare the base of the database sessions.
Base = declarative_base()
Base.query = database_session.query_property()

# We must import all the models first and then we bind the base to our engine.
def init_database():
    import models
    Base.metadata.create_all(bind=engine)
