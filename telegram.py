import os
import time
import telebot
import json
from telebot import types
from db import DbServices
from flask import Blueprint, request, render_template, session, abort


app_telegram = Blueprint('app_telegram',__name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        'Hello, ' + message.from_user.first_name + '!')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Need help?')


@bot.message_handler(commands=['oos'])
def oos(message):
    brand_names = ['Brand 1', 'Brand 2', 'Brand 3', 'Brand 4', 'Brand 5']

    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in brand_names])
    msg = bot.send_message(message.chat.id, 'Please select brand', reply_markup=keyboard)
    
    bot.register_next_step_handler(msg, oos_next_step)


def oos_next_step(message):
    bot.send_message(message.chat.id, 'You selected ' + message.text)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def echo_message(message):
    db = DbServices()
    db.callproc('add_item', (
        int(time.time()),
        message.location.latitude,
        message.location.longitude))
    db.commit()
    bot.send_message(message.chat.id, 
    	str(message.location.latitude) + ', ' + str(message.location.longitude))


@app_telegram.route("/telegram/" + os.environ.get('TELEGRAM_BOT_TOKEN'), methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app_telegram.route("/telegram/set_webhook")
def set_webhook():
    bot.remove_webhook()
    bot.set_webhook(url=os.environ.get('BASE_URL') 
        + "/telegram/" + os.environ.get('TELEGRAM_BOT_TOKEN'))
    return "!", 200


@app_telegram.route("/telegram/remove_webhook")
def remove_webhook():
    bot.remove_webhook()
    return "!", 200