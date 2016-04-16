import sqlite3

class Database:

    def __init__(self, database):
        print 'Initializing the database.'

    def save(self):
        print 'Saving a new object.'

    def get_objects(self):
        print 'Doing a general query in the database.'

    def remove_objects(self):
        print 'Removing all objects.'

    # Private methods

    def _create_table(self):
        print 'Creating the database with a private method.'
