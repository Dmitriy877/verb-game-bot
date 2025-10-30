import random
import logging

from logging.handlers import RotatingFileHandler
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import env
from dialogflow_bot import detect_intent_texts
import telegram 
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


env.read_env()
PROJECT_ID = env.str("Project_ID")
LANGUAGE_CODE = "en-US"
VK_API_KEY = env.str('VK_API_KEY')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, log_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.log_bot = log_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.log_bot.send_message(chat_id=self.chat_id, text=log_entry)


def echo(event, vk_api):
    session_id = event.user_id
    text = [event.text]
    answer = detect_intent_texts(PROJECT_ID, session_id, text, LANGUAGE_CODE)
    if answer:
        vk_api.messages.send(
            user_id=event.user_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )


def main():
    env.read_env()
    telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
    chat_id = env.str('TELEGRAMM_CHAT_ID')
    VK_API_KEY = env.str('VK_API_KEY')

    log_bot = telegram.Bot(token=telegram_bot_token)

    logger = logging.getLogger('vk_bot_loger')
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler('vk_bot_log.log', maxBytes=200, backupCount=2)
    logger.addHandler(handler)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    while True:
        try:
            logger.info('VK Bot is working')
            vk_session = vk.VkApi(token=VK_API_KEY)
            vk_api = vk_session.get_api()
            longpoll = VkLongPoll(vk_session)
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    echo(event, vk_api)
        except Exception as error:
            logger.error('VK Bot has been crashed')
            logger.error(error, exc_info=True)


if __name__ == '__main__':
    main()