import random

import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import env
from dialogflow_bot import detect_intent_texts

env.read_env()
PROJECT_ID = env.str("Project_ID")
LANGUAGE_CODE = "en-US"


def echo(event, vk_api):
    session_id = event.user_id
    text = [event.text]
    answer = detect_intent_texts(PROJECT_ID, session_id, text, LANGUAGE_CODE)
    vk_api.messages.send(
        user_id=event.user_id,
        message=answer,
        random_id=random.randint(1, 1000)
    )


def main():

    env.read_env()
    VK_API_KEY = env.str('VK_API_KEY')

    vk_session = vk.VkApi(token=VK_API_KEY)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            echo(event, vk_api)


if __name__ == '__main__':
    main()