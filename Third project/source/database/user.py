import sqlite3
from database import Database

def User(Database):

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        self._create_table()

    def add(self, name, nfc):
        print "Adding a new user."

        # self.cursor.execute('INSERT INTO User (name, nfc)' +
        # 'VALUES (?, ?)', (name, nfc))
        # self.database.commit()

    def save(self):
        print "Saving a new User."

    def get_users(self):
        print "Getting all the users."

        # self.cursor.execute('SELECT * FROM Users')
        #
        # return self.cursor.fetchall()

    # Specific getters and setters.

    def get_name(self):
        print "Getting the name."

    def set_name(self):
        print "Setting the name."

    def get_nfc(self):
        print "Getting the NFC."

    def set_nfc(self):
        print "Setting the NFC."

    # Private methods

    def _create_table(self):
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Users (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              name TEXT NOT NULL UNIQUE,
              nfc TEXT NOT NULL
            );'''
        )
