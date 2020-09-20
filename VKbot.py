from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import date
import requests
from bs4 import BeautifulSoup
#from PY_32_VK_photos_backuper_VK_interface import VKUser
from tokens import TOKEN_VK, VK_API_KEY, VK_SOI_ID
#from starter import answer

OAUTH_VK_URL = 'https://oauth.vk.com/authorize'
NL = '\n'


class VkBot:

    def __init__(self, user_id):
        #self.VKUser_0 = VKUser(TOKEN_VK, user_id)
        print(f"{NL}Создан объект бота для пользователя с ID: {user_id}!")
        self._USER_ID = user_id
        self._USERNAME = self.get_first_name(self._USER_ID)
        #self._COMMANDS = ["ПРИВЕТ", "ПОГОДА", "ВРЕМЯ", "ПОКА"] # погода парсится неверно
        self._COMMANDS = ["СЕКС", "ВОЗРАСТ ОТ", "ВОЗРАСТ ДО", "ПОЛ", "ГОРОД", "ПРЕРВАТЬ", "ПРОДОЛЖИТЬ"]
        self.get_age(5346546)
        self.dating_questionnaire = []

    def get_first_name(self, user_id):
        """ The function that getting VK user first name """
        user = vk.method("users.get", {"user_ids": self._USER_ID})
        first_name = user[0].get('first_name')
        return first_name

    def get_second_name(self, user_id):
        """ The function that getting VK user second (last) name """
        user = vk.method("users.get", {"user_ids": self._USER_ID})
        second_name = user[0].get('last_name')
        return second_name

    def get_age(self, user_id):
        """ The function that calculating VK user age """
        user = vk.method("users.get", {"user_ids": user_id, "fields": 'bdate'})
        print('****', user)
        bdate = user[0].get('bdate')
        today = date.today()
        print('+++', bdate, today.year)
        #age = today.year - born.year
        #return age

    # # getting user name-BACKUP
    # def _get_user_name_from_vk_id(self, user_id):
    #     request = requests.get("https://vk.com/id" + str(user_id))
    #     #bs = bs4.BeautifulSoup(request.text, "html.parser")
    #     bs = BeautifulSoup(request.text, "html.parser")
    #     user_name = self._clean_all_tag_from_str(bs.findAll("title")[0])
    #     return user_name.split()[0]
    # getting time

    def _get_time(self):
        request = requests.get("https://my-calend.ru/date-and-time-today")
        #b = bs4.BeautifulSoup(request.text, "html.parser")
        b = BeautifulSoup(request.text, "html.parser")
        return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

    # tags clearance
    @staticmethod
    def _clean_all_tag_from_str(string_line):
        """
        Очистка строки stringLine от тэгов и их содержимых
        :param string_line: Очищаемая строка
        :return: очищенная строка
        """
        result = ""
        not_skip = True
        for i in list(string_line):
            if not_skip:
                if i == "<":
                    not_skip = False
                else:
                    result += i
            else:
                if i == ">":
                    not_skip = True

        return result


    def new_message(self, message):
        # start of questions
        # 0. СЕКС
        if message.upper() == self._COMMANDS[0]:
            self.dating_questionnaire.append(self._USER_ID)
            return f"Отлично, {self._USERNAME}! Далее вам будут заданы 4 вопроса для поиска. " \
                   f"Если вам нужно прервать опрос - наберите ПРЕРВАТЬ, для продолжения - ПРОДОЛЖИТЬ. " \
                   f"Важно точно соблюдать формат и структутру ответов! " \
                   f"Вопрос №1: напишите возраст партнера ОТ. Формат ответа: ВОЗРАСТ ОТ и " \
                   f"следующим сообщением ДВУЗНАЧНОЕ число. Например: " \
                   f"ответ 1-1: ВОЗРАСТ ОТ, ответ 1-2: 18"

        # 1. ВОЗРАСТ ОТ
        elif message.upper() == self._COMMANDS[1]:
            if int(message.upper()) > 0:
                age_from = answer
                self.dating_questionnaire.append(age_from)
                print(f'Сохранен возраст от:', self.dating_questionnaire[1])
            return f"Вопрос №2: напишите возраст партнера ДО. Формат ответа: ВОЗРАСТ ДО и " \
                   f"следующим сообщением ДВУЗНАЧНОЕ число. Например: " \
                   f"ответ 2-1: ВОЗРАСТ ДО" \
                   f"ответ 2-2: 25"

        # 2. ВОЗРАСТ ДО
        elif message.upper() == self._COMMANDS[2]:
            age_to = answer
            self.dating_questionnaire.append(age_to)
            print(f'Сохранен возраст до:', self.dating_questionnaire[2])
            return f"Вопрос №3: напишите пол партнера. Формат ответа: ПОЛ и " \
                   f"следующим сообщением МУЖ, ЖЕН или ЛЮБ. Например: " \
                   f"ответ 3-1: ПОЛ" \
                   f"ответ 2-2: ЖЕН"

        # 3. ПОЛ
        elif message.upper() == self._COMMANDS[3]:
            sex = answer
            self.dating_questionnaire.append(sex)
            print(f'Сохранен пол:', self.dating_questionnaire[3])
            return f"Вопрос №4: напишите город партнера. Формат ответа: ГОРОД и " \
                   f"следующим сообщением НАЗВАНИЕ. Например: " \
                   f"ответ 4-1: ГОРОД" \
                   f"ответ 4-2: Санкт-Петербург"

        # 4. ГОРОД
        elif message.upper() == self._COMMANDS[4]:
            city = answer
            self.dating_questionnaire.append(city)
            print(f'Сохранен город:', self.dating_questionnaire[4])
            return f"{self._USERNAME}, усаживайтесь поудобнее - сейчас вам будут представлены лучшие партнеры!"

        # 5. ПРЕРВАТЬ
        elif message.upper() == self._COMMANDS[5]:
            return f"До свидания, {self._USERNAME}. Скорее возвращайтесь!"

        # 6. ПРОДОЛЖИТЬ
        elif message.upper() == self._COMMANDS[6]:
            return f"Добрый день, {self._USERNAME}! Мы с вами остановились на " \
                   f"вопросе №{len(self.dating_questionnaire)}. Пожалуйста, для продолжения " \
                   f"введите {self._COMMANDS[len(self.dating_questionnaire)]}"

        # # weather
        # elif message.upper() == self._COMMANDS[1]:
        #     return self._get_weather()

        # *.Старт опроса
        else:
            return f"Добрый день, {self._USERNAME}. Я сваха Диана приветствую вас в группе поиска большой и светлой любви! Если вы готовы начать поиск своей судьбы немедленно - напишите в ответ: секс"

    # ###BACKUP_copy
    # def new_message(self, message):
    #     # hello
    #     if message.upper() == self._COMMANDS[0]:
    #         return f"Добрый день, {self._USERNAME}!"
    #
    #     # # weather
    #     # elif message.upper() == self._COMMANDS[1]:
    #     #     return self._get_weather()
    #
    #     # Time
    #     elif message.upper() == self._COMMANDS[1]:
    #         return self._get_time()
    #
    #     # Bye
    #     elif message.upper() == self._COMMANDS[2]:
    #         return f"До свидания, {self._USERNAME}!"
    #
    #     else:
    #         return "Не понимаю о чем вы, пожалуйста, переформулируйте ваш запрос"

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