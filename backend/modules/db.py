from os import environ
import psycopg2 as pg

class DB():
    def __init__(self):
        #self.conn = pg.connect(database=environ.get('DB_NAME'), user=environ.get('DB_USER'), password=environ.get('DB_PASSWORD'))
        self.conn = pg.connect(database='task-list', user='postgres', password='pgsql@kieroth29')
        self.cursor = self.conn.cursor()
        
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()