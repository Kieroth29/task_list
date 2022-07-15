from os import environ
import psycopg2 as pg

class DB():
    def __init__(self):
        self.conn = pg.connect(host="db", database=environ.get('DB_NAME'), user=environ.get('DB_USER'), password=environ.get('DB_PASSWORD'))
        self.cursor = self.conn.cursor()
        
    def __del__(self):
        self.conn.close()
        
    def commit(self):
        self.conn.commit()
        
    def close(self):
        self.conn.close()
        
    def fetchone(self):
        return self.cursor.fetchone()
    
    def fetchall(self):
        return self.cursor.fetchall()