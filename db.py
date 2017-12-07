import postgresql

class DataContext:
    db = None

    def __init__(self):
        db = postgresql.open(os.environ.get('DATABSE_URL'))


	def query(top):
        ins = db.prepare("INSERT INTO items(latitude, longitude, date) VALUES ($1, $2, $3)")
        ins(params.latitude
        	params.longitude,
        	params.date)


    def create(params)
        return db.query("SELECT * FROM items")


    def __del__(self):
        db.close()
