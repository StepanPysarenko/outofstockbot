import telebot #pyTelegramBotAPI
import os
from flask import Flask, request
# import postgresql


bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
server = Flask(__name__)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.reply_to(message, 'Hello, ' + message.from_user.first_name + '. Need help?')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.reply_to(message, message.text)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def echo_message(message):
	latitude = message.location.latitude
	longitude = message.location.longitude
	date = message.date

	# db = postgresql.open(os.environ.get('DATABASE_URL'))
	# ins = db.prepare("INSERT INTO items(latitude, longitude, date) VALUES ($1, $2, $3)")
	# ins(latitude, longitude, date)

    bot.reply_to(message, str(latitude) + ', ' + str(longitude))


@server.route("/hook", methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


# @server.route("/items")
# def get_items():
# 	items = db.query("SELECT latitude, longitude, date FROM items ORDER BY date DESC");
#     return items


@server.route("/")
def webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('HOOK_URL'))
    return "!", 200


@server.route('/helloworld')
def hello_world():
    return 'Hello, World!'


server.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
