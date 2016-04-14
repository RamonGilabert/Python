from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

engine = create_engine('sqlite:////tmp/orm_users.db', convert_unicode=True)
database_session = scoped_session(sessionmaker(autocommit=False,
autoflush=False, bind=engine))

Base = declarative_base()
Base.query = database_session.query_property()

def init_database():
    import models
    Base.metadata.create_all(bind=engine)
