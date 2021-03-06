from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from VKbot import VkBot

from tokens import TOKEN_VK, VK_API_KEY, VK_SOI_ID
#TOKEN_VK = input('Введите токен приложения ВК (TOKEN_VK): ')
#VK_API_KEY = input('Введите токен API (VK_API_KEY): ')

# Authorization as group
vk = vk_api.VkApi(token=VK_API_KEY)

# work with messages
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
print("Сервис запущен!")

# main cycle
for event in longpoll.listen():
    # if we get new message
    if event.type == VkEventType.MESSAGE_NEW:

        # if message for bot
        if event.to_me:
            # message from user
            #request = event.text # version #1
            print(f'Новое сообщение от {event.user_id}', end='')
            bot = VkBot(event.user_id)
            write_msg(event.user_id, bot.new_message(event.text))
            global answer
            answer = event.text
            print('Text: ', answer)
            print("-------------------")






