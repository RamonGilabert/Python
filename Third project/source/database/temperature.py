import sqlite3
from database import Database

class Temperature(Database):

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        self._create_table()
        self._instantiate_variables()

    def add(self, temperature, created, difference, user_nfc):
        print "Adding a new tempreature."

        self.cursor.execute('INSERT INTO Temperatures (temperature, created, \
        difference, user_nfc)' + 'VALUES (?, ?, ?, ?)', \
        (temperature, created, difference, user_nfc))
        self.database.commit()

    def save(self):
        if self._temperature == None \
        or self._created == None \
        or self._difference == None \
        or self._user_nfc == None:
            return 'You need to set all the properties.'
        else:
            self.add(self._temperature, self._created, \
            self._difference, self._user_nfc)
            self._instantiate_variables()
        return None

    def get_objects(self):
        print "Getting all the temperatures."

        self.cursor.execute('SELECT * FROM Temperatures')
        return self.cursor.fetchall()

    def remove_objects(self):
        print 'Removing all temperatures.'
        self.cursor.execute('DELETE FROM Temperatures')

    # Specific getters and setters.

    def get_temperature(self):
        return self._temperature

    def set_tempreature(self, temperature):
        self._temperature = temperature

    def get_created(self):
        return self._created

    def set_created(self, created):
        self._created = created

    def get_difference(self):
        return self._difference

    def set_difference(self, difference):
        self._difference = diference

    def get_user(self):
        return self._user_id

    def set_user(self, user_nfc):
        self._user_nfc = _user_nfc

    # Private methods

    def _create_table(self):
        print 'Creating the Temperature table.'

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS Temperatures (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              temperature FLOAT NOT NULL,
              created DATE NOT NULL,
              difference FLOAT,
              user_nfc INT NOT NULL,
              FOREIGN KEY (user_nfc) REFERENCES Users(nfc)
            );'''
        )

    def _instantiate_variables(self):
        self._temperature = None
        self._created = None
        self._difference = None
        self._user_nfc = None
