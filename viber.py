import os
import time
from viberbot import Api
from viberbot.api.bot_configuration import BotConfiguration
from viberbot.api.messages import VideoMessage,  LocationMessage
from viberbot.api.messages.data_types.location import Location
from viberbot.api.messages.text_message import TextMessage
from viberbot.api.viber_requests import ViberMessageRequest, ViberSubscribedRequest, \
    ViberUnsubscribedRequest, ViberConversationStartedRequest, ViberFailedRequest
from flask import Blueprint, request
from db import DbServices


app_viber = Blueprint('app_viber', __name__)


bot_configuration = BotConfiguration(
    name=os.environ.get('VIBER_BOT_NAME'),
    avatar='http://cte.tamu.edu/getattachment/Fellows-and-Scholars/Montague-CTE-Scholars/Past-Years-Scholars/1995-1996-Scholars/temporary-profile-placeholder-(1).jpg.aspx',
    auth_token=os.environ.get('VIBER_BOT_TOKEN'))
bot = Api(bot_configuration)


@app_viber.route('/' + os.environ.get('VIBER_BOT_TOKEN'), methods=['POST'])
def incoming():
    viber_request = bot.parse_request(request.get_data())

    if isinstance(viber_request, ViberMessageRequest):
        if isinstance(viber_request.message, LocationMessage):
            save_location(viber_request.message)
            bot.send_messages(viber_request.sender.id, [
                TextMessage(text=str(viber_request.message.location.latitude)
                            + ', ' + str(viber_request.message.location.longitude))
            ])
        else:
            bot.send_messages(viber_request.sender.id, [viber_request.message])

    elif isinstance(viber_request, ViberSubscribedRequest):
        bot.send_messages(viber_request.get_user.id, [
            TextMessage(text="Thanks for subscribing!")
        ])

    return "!", 200


def save_location(message):
    db = DbServices()
    db.callproc('add_item', (
        int(time.time()),
        message.location.latitude,
        message.location.longitude))
    db.commit()


@app_viber.route('/set_webhook')
def set_webhook():
    bot.set_webhook(os.environ.get('VIBER_HOOK_URL'))
    return "!", 200


@app_viber.route('/remove_webhook')
def remove_webhook():
    bot.unset_webhook()
    return "!", 200

