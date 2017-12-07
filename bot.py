import telegram.bot.bot as bot_telegram
from flask import Flask, request

app = Flask(__name__)


@app.route("/hook", methods=['POST'])
bot_telegram.process_new_updates()


@app.route("/set_webhook")
bot_telegramset_webhook()


@app.route("/remove_webhook")
bot_telegram.remove_webhook()


app.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
