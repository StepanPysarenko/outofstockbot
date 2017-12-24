import os
import json
import datetime
from db import DbServices
from flask import Blueprint, request, render_template, session, abort


app = Blueprint('app_results', __name__)


@app.route("/items")
def get_items():
    items = map(lambda item: {
        "id": item[0],
        "date": datetime.datetime.fromtimestamp(item[1]).strftime('%Y-%m-%d %H:%M:%S'),
        "latitude": item[2],
        "longitude": item[3],
        "link": "http://www.google.com/maps/place/{0},{1}".format(item[2], item[3])
    }, DbServices().callproc('get_items', (0, 1000,)))
    return render_template('items.html', items=items)

