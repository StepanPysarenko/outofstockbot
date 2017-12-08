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


    def query_items(self):
        self.cur.execute("""
            SELECT 
                id,
                date,
                trim(to_char(latitude, '99D999999')),
                trim(to_char(longitude, '99D999999'))
            FROM items 
            ORDER BY date DESC 
            LIMIT 100
            """)
        items = self.cur.fetchall()
        return "<pre>" + json.dumps(items, sort_keys=True, 
            indent=4, separators=(',', ': ')) + "</pre>"


    def __del__(self):
        self.conn.close()
