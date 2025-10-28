import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from environs import env


def main():

    env.read_env()
    VK_API_KEY = env.str('VK_API_KEY')

    vk_session = vk_api.VkApi(token=VK_API_KEY)
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW:
            print('Новое сообщение:')
            if event.to_me:
                print('Для меня от: ', event.user_id)
            else:
                print('От меня для: ', event.user_id)
            print('Текст:', event.text)


if __name__ == '__main__':
    main()