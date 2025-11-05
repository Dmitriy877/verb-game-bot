import random
import logging

from logging.handlers import RotatingFileHandler
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import env
from dialogflow_bot import detect_intent_texts
import telegram 


class TelegramLogsHandler(logging.Handler):
    def __init__(self, log_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.log_bot = log_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.log_bot.send_message(chat_id=self.chat_id, text=log_entry)


def send_message(event, vk_api, project_id, language_code):
    dialogflow_chat_id = f'vk-{event.user_id}'
    chat_id = event.user_id
    text = [event.text]
    answer = detect_intent_texts(project_id, dialogflow_chat_id, text, language_code)
    if answer:
        vk_api.messages.send(
            user_id=chat_id,
            message=answer,
            random_id=random.randint(1, 1000)
        )
    else:
        vk_api.messages.send(
            user_id=chat_id,
            message='Я Вас не понял, сейчас позову оператора',
            random_id=random.randint(1, 1000)
        )


def main():
    env.read_env()
    env.read_env()
    project_id = env.str("PROJECT_ID")
    language_code = env.str("LANGUAGE_CODE")
    telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
    chat_id = env.str('TELEGRAMM_CHAT_ID')
    vk_api_key = env.str('VK_API_KEY')

    log_bot = telegram.Bot(token=telegram_bot_token)
    logger = logging.getLogger('vk_bot_loger')
    logger.setLevel(logging.INFO)
    logger.addHandler(RotatingFileHandler('vk_bot_log.log', maxBytes=200, backupCount=2))
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    vk_session = vk.VkApi(token=vk_api_key)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_message(event, vk_api, project_id, language_code)
    except Exception as error:
        logger.exception(f'VK Bot Has been crashed with error {error}')


if __name__ == '__main__':
    main()