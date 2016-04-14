import sqlite3
from flask import g
from contextlib import closing

# This is the main class for the connection to the database, I preferred
# to have a different class to practica OOP and also to just separate
# concerns from the routes.

class Connection:

    def __init__(self, app):
        self.app = app

    # Get users will do a query ot the database requesting all the information
    # with the * and just give you what you need in an object format.
    def get_users(self):
        execution = g.db.execute('SELECT * FROM Users')
        users = [dict(name=row[2], email=row[3], username=row[1]) for row in execution.fetchall()]
        return users

    # This will connect to the database into the app config stated in the app
    # file.
    def connect_database(self):
        return sqlite3.connect(self.app.config['DATABASE'])

    # This will initialize the database based on the configuration that we have
    # in the schema.sql file in mode ride.
    def init_database(self):
        with closing(self.connect_database()) as database:
            with self.app.open_resource('schema.sql', mode='r') as f:
                database.cursor().executescript(f.read())
                database.commit()
