import logging
from environs import env
from telegram import Update

from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def detect_intent_texts(project_id, session_id, texts, language_code):
    """Returns the result of detect intent with texts as inputs.

    Using the same `session_id` between requests allows continuation
    of the conversation."""
    from google.cloud import dialogflow

    session_client = dialogflow.SessionsClient()

    session = session_client.session_path(project_id, session_id)
    print("Session path: {}\n".format(session))

    for text in texts:
        text_input = dialogflow.TextInput(text=text, language_code=language_code)

        query_input = dialogflow.QueryInput(text=text_input)

        response = session_client.detect_intent(
            request={"session": session, "query_input": query_input}
        )

        print("=" * 20)
        print("Query text: {}".format(response.query_result.query_text))
        print(
            "Detected intent: {} (confidence: {})\n".format(
                response.query_result.intent.display_name,
                response.query_result.intent_detection_confidence,
            )
        )
        print("Fulfillment text: {}\n".format(response.query_result.fulfillment_text))


def main():

    env.read_env()
    project_id = env.str("PROJECT_ID")
    session_id = env.str("SESSION_ID")
    texts = ['Привет!']
    language_code = "ru-RU"
    detect_intent_texts(project_id, session_id, texts, language_code)

    # telegram_bot_token = env.str('TELEGRAM_BOT_TOKEN')

    # updater = Updater(token=telegram_bot_token)
    # dispatcher = updater.dispatcher

    # logging.basicConfig(
    #     format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    #     level=logging.INFO
    # )

    # start_handler = CommandHandler('start', start)
    # echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)

    # dispatcher.add_handler(start_handler)
    # dispatcher.add_handler(echo_handler)
    # updater.start_polling()


if __name__ == '__main__':
    main()
