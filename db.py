import os
import psycopg2

class DbServices:
    conn = None
    cur = None

    def __init__(self):
        conn =psycopg2.connect(os.environ.get('DATABASE_URL'))
        cur = conn.cursor()


    def create_item(params):
        cur.execute("INSERT INTO items(latitude, longitude, date) VALUES (%s, %s, %s)", 
        	(params.latitude, params.longitude, params.date))


    def query_items():
    	cur.execute("SELECT * FROM items ORDER BY date DESC")
		return cur.fetchall()


    def __del__(self):
        conn.close()
