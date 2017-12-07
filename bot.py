import bot_telegram
from flask import Flask, request

app = Flask(__name__)



@server.route("/hook", methods=['POST'])
bot_telegram.bot.process_new_updates()


@server.route("/set_webhook")
bot_telegram.bot.set_webhook()


@server.route("/remove_webhook")
bot_telegram.bot.remove_webhook()


server.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
