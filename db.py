import os
import psycopg2
from psycopg2 import extras


class DbServices:
    conn = None
    cur = None


    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cur = self.conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

        
    def query(self, query, args=()):
        self.cur.execute(query, args)
        return self.__fetchcursor()


    def callproc(self, name, args=()):
        self.cur.callproc(name, args)
        return self.__fetchcursor()


    def __fetchcursor(self):
        return self.cur.fetchall() if (self.cur.description is not None) else None


    def commit(self):
        self.conn.commit()


    def __del__(self):
        self.cur.close()
        self.conn.close()
