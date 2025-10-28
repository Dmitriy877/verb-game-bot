import logging

from environs import env
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from dialogflow_bot import detect_intent_texts

env.read_env()
PROJECT_ID = env.str("Project_ID")
LANGUAGE_CODE = "en-US"


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def bot_message(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    text = [update.message.text]
    chat_id = update.effective_chat.id
    answer = detect_intent_texts(PROJECT_ID, chat_id, text, LANGUAGE_CODE)
    if answer:
        context.bot.send_message(chat_id=chat_id, text=answer)
    else:
        context.bot.send_message(chat_id=chat_id, text='Ничего не понял, но очень интересно!')


def main():

    env.read_env()

    telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')

    updater = Updater(token=telegram_bot_token)
    dispatcher = updater.dispatcher

    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    start_handler = CommandHandler('start', start)
    echo_handler = MessageHandler(Filters.text & (~Filters.command), bot_message)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(echo_handler)
    updater.start_polling()


if __name__ == '__main__':
    main()
