import os
import psycopg2


class DbServices:

    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cur = self.conn.cursor()


    def create_item(self, params):
        self.cur.execute("INSERT INTO items(latitude, longitude, date) VALUES (%s, %s, %s)", 
            (params.latitude, params.longitude, params.current_date))


    def query_items(self):
        self.cur.execute("SELECT * FROM items ORDER BY date DESC")
        return self.cur.fetchall()


    def __del__(self):
        self.conn.close()
