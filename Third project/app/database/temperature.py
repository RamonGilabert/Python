import sqlite3

def Temperature:

    def __init__(self, database):
        self.database = sqlite3.connect(database)
        self.database.row_factory = sqlite3.Row
        self.cursor = self.db.cursor()

    def add(self, temperature, created, difference, user_id):
        print "Adding a new tempreature."

        # self.cursor.execute('INSERT INTO Temperature (temperature, created, difference, user_id)' +
        # 'VALUES (?, ?, ?, ?)', (temperature, created, difference, user_id))
        # self.database.commit()

    def save(self):
        print "Saving a new Temperature."

    def get_users(self):
        print "Getting all the temperatures."

        # self.cursor.execute('SELECT * FROM Temperature')
        #
        # return self.cursor.fetchall()

    # Specific getters and setters.

    def get_temperature(self):
        print "Getting the tempreature."

    def set_tempreature(self):
        print "Setting the temperature."

    def get_created(self):
        print "Getting the date."

    def set_created(self):
        print "Setting the date."

    def get_difference(self):
        print "Getting the difference."

    def set_created(self):
        print "Setting the difference."

    def get_user(self):
        print "Getting the user"

    def set_user(self):
        print "Setting the user"
