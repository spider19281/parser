import sqlite3

class Database:
    def __init__(self):
        self.connection = sqlite3.connect('./database.db')
        self.cursor = self.connection.cursor()

    def insert_item(self, item):
        cur = self.cursor.execute(
            "insert into posts (title, file, link) values (?, ?, ?)",
                (item['title'], item['file'], item['link']))
        self.connection.commit()
    
    def close(self):
        self.connection.close()