import sqlite3

class Database(object):

    def __init__(self, database, table):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.database.cursor()
        self.table = table

    def get_objects(self):
        self.cursor.execute('SELECT * FROM ' + self.table)
        return self.cursor.fetchall()

    def remove_objects(self):
        self.cursor.execute('DELETE FROM ' + self.table)

    # Private methods

    def _create_table(self):
        print 'Create the table in the database.'

    def _instantiate_variables(self):
        print 'Add the initial behavior of the variables.'
