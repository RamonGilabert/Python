import sqlite3
from database import Database

class User(Database):

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        self._create_table()
        self._name = None
        self._nfc = None

    def add(self, name, nfc):
        print "Adding a new user."

        self.cursor.execute('INSERT INTO Users (name, nfc)' +
        'VALUES (?, ?)', (name, nfc))
        self.database.commit()

    def save(self):
        if self._name == None or self._nfc == None:
            return 'You need to set all the properties.'
        else:
            print 'Hey'
        return None

    def get_objects(self):
        print "Getting all the users."

        self.cursor.execute('SELECT * FROM Users')

        return self.cursor.fetchall()

    def remove_objects(self):
        print 'Removing all temperatures.'
        self.cursor.execute('DELETE FROM Users')

    # Specific getters and setters.

    def get_name(self):
        return self._name

    def set_name(self, name):
        self._name = name

    def get_nfc(self):
        return self._nfc

    def set_nfc(self, nfc):
        self._nfc = nfc

    # Private methods

    def _create_table(self):
        print 'Creating the Users table.'

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Users (
              nfc TEXT PRIMARY KEY NOT NULL,
              name TEXT NOT NULL
            );'''
        )
