import telebot
import os
from flask import Flask, request

from db import DbServices

app = Flask(__name__)
bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Hello, ' + message.from_user.first_name)


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Need help?')


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def echo_message(message):
    db_services = DbServices()
    db_services.create_item({
        date: message.date, 
        latitude: message.location.latitude,
        longitude: message.location.longitude
        })
    bot.send_message(message.chat.id, 
    	str(message.location.latitude) + ', ' + str(message.location.longitude))


@app.route("/hook", methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app.route("/set_webhook")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('HOOK_URL'))
    return "!", 200


@app.route("/remove_webhook")
def remove_webhook():
    bot.remove_webhook()
    return "!", 200

@app.route("/items")
    def get_results():
    db_services = DbServices()
    items = db_services.query_items()
    return items, 200


app.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
