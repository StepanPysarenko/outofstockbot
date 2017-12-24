import os
import json
from flask import Flask, render_template
from db import DbServices
from telegram import app_telegram
from viber import app_viber
from jinja2 import Template

app = Flask(__name__)
app.register_blueprint(app_telegram)
app.register_blueprint(app_viber)


@app.route("/items")
def get_items():
    items = DbServices().callproc('get_items', (0, 100,))
    # items = DbServices().callproc('get_items', (0, 100,))
    # result = "<pre>" + json.dumps(items, sort_keys=True,
    #     indent=4, separators=(',', ': ')) + "</pre>"
    # return result, 200
    # template = Template('Hello {{ name }}!')
    # return template.render(name='John Doe')
    return render_template('items.html', items=items)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
