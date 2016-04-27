import sqlite3
from database import Database

class User(Database):

    def __init__(self, database):
        super(User, self).__init__(database, 'Users')
        self._create_table()
        self._instantiate_variables()

    def add(self, name, nfc):
        users = self.get_objects()
        should_add_user = True

        for user in users:
            if user['nfc'] == nfc:
                should_add_user = False
                break

        if should_add_user:
            self.cursor.execute('INSERT INTO Users (name, nfc)'
            + 'VALUES (?, ?)', (name, nfc))
            self.database.commit()

    def save(self):
        if self._name == None or self._nfc == None:
            return 'You need to set all the properties.'
        else:
            self.add(self._name, self._nfc)
            self._instantiate_variables()
        return None

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

    def _instantiate_variables(self):
        self._name = None
        self._nfc = None
