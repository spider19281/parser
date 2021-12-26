import sqlite3

class Database(object):
    def __init__(self):
        self.connection = sqlite3.connect('./database.db')
        self.cursor = self.connection.cursor()

    def commit(self):
        self.connection.commit()
    
    def close(self):
        self.connection.close()