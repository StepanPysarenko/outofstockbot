import os
import time
import telebot
from telebot import types
from db import DbServices
from flask import Blueprint, request


app_telegram = Blueprint('app_telegram', __name__)

bot = telebot.TeleBot(os.environ.get('TELEGRAM_BOT_TOKEN'))


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 
        'Hello, ' + message.from_user.first_name + '!')


@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, 'Need help?')


@bot.message_handler(commands=['oos'])
def oos_step_1(message):
    names = ['Item 1', 'Item 2', 'Item 3', 'Item 4', 'Item 5']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in names])
    msg = bot.send_message(message.chat.id, 'Please select item', 
        reply_markup=keyboard)
    
    bot.register_next_step_handler(msg, oos_step_2)


def oos_step_2(message):
    names = [message.text + '.1', message.text + '.2']
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(*[types.KeyboardButton(name) for name in names])
    msg = bot.send_message(message.chat.id, 'Please select subitem', 
        reply_markup=keyboard)   
    bot.register_next_step_handler(msg, oos_step_3)


def oos_step_3(message):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Code"))
    keyboard.add(types.KeyboardButton("Location", request_location=True))   
    msg = bot.send_message(message.chat.id, 'You selected ' + message.text,
        reply_markup=keyboard)
    bot.register_next_step_handler(msg, oos_step_4)


def oos_step_4(message):
    save_location(message)
    markup = types.ReplyKeyboardRemove(selective=False)
    bot.send_message(message.chat.id, 
        str(message.location.latitude) + ', ' + str(message.location.longitude),
        reply_markup=markup)


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, message.text)


@bot.message_handler(func=lambda message: True, content_types=['location'])
def location_message(message):
    save_location(message)
    bot.send_message(message.chat.id,
    	str(message.location.latitude) + ', ' + str(message.location.longitude))


def save_location(message):
    db = DbServices()
    db.callproc('add_item', (
        int(time.time()),
        message.location.latitude,
        message.location.longitude))
    db.commit()


@app_telegram.route('/' + os.environ.get('TELEGRAM_BOT_TOKEN'), methods=['POST'])
def webhook():
    bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
    return "!", 200


@app_telegram.route('/set_webhook')
def set_webhook():
    bot.set_webhook(url=os.environ.get('TELEGRAM_HOOK_URL'))
    return "!", 200


@app_telegram.route('/remove_webhook')
def remove_webhook():
    bot.remove_webhook()
    return "!", 200