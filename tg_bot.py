import logging

from functools import partial
from logging.handlers import RotatingFileHandler
from environs import env
import telegram 
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dialogflow_bot import detect_intent_texts


class TelegramLogsHandler(logging.Handler):
    def __init__(self, log_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.log_bot = log_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.log_bot.send_message(chat_id=self.chat_id, text=log_entry)


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def send_message(update: Update, context: CallbackContext, LANGUAGE_CODE, PROJECT_ID) -> None:
    """Echo the user message."""
    text = [update.message.text]
    dialogflow_chat_id = f'tg-{update.effective_chat.id}'
    chat_id = update.effective_chat.id

    answer = detect_intent_texts(PROJECT_ID, dialogflow_chat_id, text, LANGUAGE_CODE)
    if answer:
        context.bot.send_message(chat_id=chat_id, text=answer)
    else:
        context.bot.send_message(chat_id=chat_id, text='Ничего не понял, но очень интересно!')


def main():

    env.read_env()
    PROJECT_ID = env.str("PROJECT_ID")
    LANGUAGE_CODE = env.str("LANGUAGE_CODE")
    telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')
    chat_id = env.str('TELEGRAMM_CHAT_ID')
    send_message_with_arguments = partial(send_message, LANGUAGE_CODE=LANGUAGE_CODE, PROJECT_ID=PROJECT_ID)

    log_bot = telegram.Bot(token=telegram_bot_token)
    logger = logging.getLogger('tg_bot_loger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))
    logger.addHandler(RotatingFileHandler('tg_bot_log.log', maxBytes=200, backupCount=2))

    updater = Updater(token=telegram_bot_token)
    dispatcher = updater.dispatcher

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), send_message_with_arguments)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)

    try:
        updater.start_polling()
    except Exception as error:
        logger.exception(f'TG Bot Has been crashed with error {error}')


if __name__ == '__main__':
    main()
