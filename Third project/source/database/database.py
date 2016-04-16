import sqlite3

class Database(object):

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()

    def save(self):
        print 'Saving a new object.'

    def get_objects(self, table):
        self.cursor.execute('SELECT * FROM ' + table)
        return self.cursor.fetchall()

    def remove_objects(self, table):
        self.cursor.execute('DELETE FROM ' + table)

    # Private methods

    def _create_table(self):
        print 'Creating the database with a private method.'

    def _instantiate_variables(self):
        print 'Add the initial behavior of the variables.'
