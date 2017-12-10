import os
import json
from flask import Flask
from db import DbServices
from telegram import app_telegram
from viber import app_viber


app = Flask(__name__)
app.register_blueprint(app_telegram)
app.register_blueprint(app_viber)


@app.route("/items")
def get_items():
    items = DbServices().callproc('get_items', (100,))
    result = "<pre>" + json.dumps(items, sort_keys=True,
        indent=4, separators=(',', ': ')) + "</pre>"
    return result, 200


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))