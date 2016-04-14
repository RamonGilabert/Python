import sqlite3
from flask import g
from contextlib import closing

class Connection:

    def __init__(self, app):
        self.app = app

    def get_users(self):
        execution = g.db.execute('SELECT * FROM Users')
        users = [dict(name=row[2], email=row[3], username=row[1]) for row in execution.fetchall()]
        return users

    def connect_database(self):
        return sqlite3.connect(self.app.config['DATABASE'])

    def init_database(self):
        with closing(self.connect_database()) as database:
            with self.app.open_resource('schema.sql', mode='r') as f:
                database.cursor().executescript(f.read())
                database.commit()
