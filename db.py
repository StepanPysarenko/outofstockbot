import os
import psycopg2
import json


class DbServices:

    def __init__(self):
        self.conn = psycopg2.connect(os.environ.get('DATABASE_URL'))
        self.cur = self.conn.cursor()


    def create_item(self, params):
        self.cur.execute("""
            INSERT INTO items(date, latitude, longitude) 
            VALUES (%s, %s, %s)
            """, 
            (params['date'], params['latitude'], params['longitude']))
        self.conn.commit()


    def query_db(self, query, args=(), one=False):
        self.cur.execute(query, args)
        r = [dict((cur.description[i][0], value) \
                   for i, value in enumerate(row)) for row in cur.fetchall()]
        self.cur.connection.close()
        return (r[0] if r else None) if one else r


    def query_items(self):
        result = self.query_db("""
            SELECT *
            FROM items 
            ORDER BY date DESC 
            LIMIT 100
            """)
        return "<pre>" + json.dumps(result, sort_keys=True, 
            indent=4, separators=(',', ': ')) + "</pre>"


    def __del__(self):
        self.conn.close()
