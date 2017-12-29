import os
from flask import Flask
from telegram import app_telegram
from viber import app_viber
from results import app_results

app = Flask(__name__)
app.register_blueprint(app_telegram, url_prefix='/telegram')
app.register_blueprint(app_viber, url_prefix='/viber')
app.register_blueprint(app_results, url_prefix='/results')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=os.environ.get('PORT'))
