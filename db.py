import os
import psycopg2


class DbServices:
    conn = None
    cur = None

    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cur = self.conn.cursor()

        
    def query(self, query, args=()):
        return self.cur.execute(query, args).fetchall()


    def callproc(self, name, args=()):
        return self.cur.callproc(name, args).fetchall()


    def commit():
        self.conn.commit()


    def __del__(self):
        self.cur.close()
        self.conn.close()
