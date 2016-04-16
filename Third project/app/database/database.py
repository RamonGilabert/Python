import sqlite3

def Database:

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        self._create_table()

    def save(self):
        print 'Saving a new object.'

    def get_objects(self):
        print 'Doing a general query in the database.'

    # Private methods

    def _create_table(self):
        print 'Creating the database with a private method.'
