import sqlite3
from flask import g
from contextlib import closing

# This is the main class for the connection to the database, I preferred
# to have a different class to practica OOP and also to just separate
# concerns from the routes.

class Connection:

    def __init__(self, app):
        self.app = app

    def get_users(self):
        execution = g.db.execute('SELECT * FROM Users')
        return [dict(nfc=row[0], name=row[0]) for row in execution.fetchall()]

    def get_temperatures(self):
        execution = g.db.execute('SELECT * FROM Temperatures')
        return [dict(temperature=row[1], created=row[2], difference=row[3]) \
            for row in execution.fetchall()]

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
