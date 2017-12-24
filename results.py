import os
import json
import datetime
from db import DbServices
from flask import Blueprint, request, render_template, session, abort


app = Blueprint('app_results', __name__)


@app.route("/items")
def get_items():

    page = 1 if (request.args.get('page') is None) else int(request.args.get('page'))
    limit = 100
    offset = (page - 1) * limit

    items = map(lambda item: {
        'id': item['id'],
        'date': datetime.datetime.fromtimestamp(item['date']).strftime('%Y-%m-%d %H:%M:%S'),
        'latitude': item['latitude'],
        'longitude': item['longitude'],
        'link': "http://www.google.com/maps/place/{0},{1}".format(item['latitude'], item['longitude'])
    }, DbServices().callproc('get_items', (offset, limit)))

    return render_template('items.html', items=items)

