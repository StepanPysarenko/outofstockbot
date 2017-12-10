import os
import json
from flask import Flask, request
from db import DbServices
from telegram import app as app_telegram
from viber import app as app_viber


app = Flask(__name__)
app.register_blueprint(app_telegram)
app.register_blueprint(app_viber)


@app.route("/items")
def get_items():
    items = DbServices().callproc('get_items', (100,))
    result = "<pre>" + json.dumps(items) + "</pre>"   
    return result, 200


app.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
