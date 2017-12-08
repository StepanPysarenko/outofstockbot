import os
from flask import Flask, request
from db import DbServices
import telegram.app_telegram
# import viber.app_viber


app = Flask(__name__)
app.register_blueprint(app_telegram)
# app.register_blueprint(app_viber)


@app.route("/items")
def get_items():
    db_services = DbServices()
    items = db_services.query_items()
    return items, 200


app.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
