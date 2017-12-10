import os
import time
import logging
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberConversationStartedRequest
from viberbot.api.viber_requests import ViberFailedRequest
from viberbot.api.viber_requests import ViberMessageRequest
from viberbot.api.viber_requests import ViberSubscribedRequest
from viberbot.api.viber_requests import ViberUnsubscribedRequest
from flask import Blueprint, request, render_template, session, abort
from db import DbServices

BOT_TOKEN = os.environ.get('VIBER_BOT_TOKEN')
BOT_NAME = 'OutOfStockBot' # os.environ.get('VIBER_BOT_NAME') 
BASE_URL = os.environ.get('BASE_URL') 
URL_PEFIX = '/viber'

app_viber = Blueprint('app_viber',__name__)


bot_configuration = BotConfiguration(
    name=BOT_NAME, auth_token=BOT_TOKEN)
bot = Api(bot_configuration)


@app_viber.route(URL_PEFIX + '/' + BOT_TOKEN, methods=['POST'])
def incoming():
    logger.debug("received request. post data: {0}".format(request.get_data()))
    # every viber message is signed, you can verify the signature using this method
    if not bot.verify_signature(request.get_data(), request.headers.get('X-Viber-Content-Signature')):
        return Response(status=403)

    # this library supplies a simple way to receive a request object
    viber_request = bot.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        message = viber_request.message
        # lets echo back
        bot.send_messages(viber_request.sender.id, [
            message
        ])
    elif isinstance(viber_request, ViberSubscribedRequest):
        bot.send_messages(viber_request.get_user.id, [
            TextMessage(text="thanks for subscribing!")
        ])
    elif isinstance(viber_request, ViberFailedRequest):
        logger.warn("client failed receiving message. failure: {0}".format(viber_request))

    return Response(status=200)


@app_viber.route(URL_PEFIX + '/set_webhook')
def set_webhook():
    bot.unset_webhook()
    bot.set_webhook(BASE_URL + URL_PEFIX + '/' + BOT_TOKEN)
    return "!", 200


@app_viber.route(URL_PEFIX + '/remove_webhook')
def remove_webhook():
    bot.unset_webhook()
    return "!", 200
