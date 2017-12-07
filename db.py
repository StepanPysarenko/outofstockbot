import os
import postgresql

class DbServices:
    db = None


    def __init__(self):
        db = postgresql.open(os.environ.get('DATABSE_URL'))


    def create_item(params):
        ins = db.prepare("INSERT INTO items(latitude, longitude, date) VALUES ($1, $2, $3)")
        ins(params.latitude, params.longitude, params.date)


    def query_items():
        return db.query("SELECT * FROM items ORDER BY date DESC")


    def __del__(self):
        db.close()
