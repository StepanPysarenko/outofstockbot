import telebot #pyTelegramBotAPI
import os
import json
from flask import Flask, request


bot = telebot.TeleBot(os.environ.get('BOT_TOKEN'))
server = Flask(__name__)


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
    bot.send_message(message.chat.id, 
    	str(message.location.latitude) + ', ' + str(message.location.longitude))


@server.route("/hook", methods=['POST'])
def get_message():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@server.route("/set_webhook")
def set_webhook():
    bot.remove_webhook()  
    return bot.set_webhook(url=os.environ.get('HOOK_URL')), 200


@server.route("/remove_webhook")
def remove_webhook():   
    return bot.remove_webhook(), 200


server.run(host="0.0.0.0", port=os.environ.get('PORT', 17995))
