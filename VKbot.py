from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import date
import requests
from users_manager import UsersManager
from db_engine import DBEngine
from db_model import User
from users_search import UsersSearch
from tokens import TOKEN_VK, VK_API_KEY, VK_SOI_ID, VK_FEDOROV_ID, VK_ADMIN_TOKEN
#from starter import answer
from collections import Counter

OAUTH_VK_URL = 'https://oauth.vk.com/authorize'
NL = '\n'


class VkBot:

    def __init__(self, token: str, user_id):
        self.token_VK = token
        print(f"{NL}Создан объект бота для пользователя с ID: {user_id}!") #заготовка под многопользовательское использование
        self._USER_ID = user_id
        self.user = users_manager_1.get_user(str(self._USER_ID))
        if self.user == None:
            self.user = User().with_(
                vk_id = self._USER_ID,
                first_name = UsersSearch.get_first_name(User.vk_id),
                last_name = UsersSearch.get_last_name(User.vk_id),
                age = UsersSearch.get_age(User.vk_id),
                age_min = User.age - 5,
                age_max = User.age + 5,
                sex = UsersSearch.get_sex(User.vk_id),
                city = UsersSearch.get_city_id(User.vk_id)
            )
            users_manager_1.save_user(self.user)
        ###BACKUP_COPY
            # if self.user == None:
            #     self.user = User().with_(vk_id=self._USER_ID)
            #     users_manager_1.save_user(self.user)

            users_manager_1.save_user(self.user)

            self._USERNAME = self.get_first_name(self._USER_ID)

        self._COMMANDS = ["СЕКС", "ВОЗРАСТ ОТ", "ВОЗРАСТ ДО", "ПОЛ", "ГОРОД", "ПРЕРВАТЬ", "ПРОДОЛЖИТЬ"]
        self.get_age(self._USER_ID)
        print('self.get_age(self._USER_ID):', self.get_age(self._USER_ID))
        self.dating_questionnaire = []
        self.answer_1_2 = False
        self.answer_2_2 = False
        self.dating_users = []
        self.likes_dic = {}

    def get_first_name(self, user_id):
        """ The function that getting VK user first name """
        user = vk.method("users.get", {"user_ids": user_id})
        first_name = user[0].get('first_name')
        return first_name

    def get_second_name(self, user_id):
        """ The function that getting VK user second (last) name """
        user = vk.method("users.get", {"user_ids": user_id})
        second_name = user[0].get('last_name')
        return second_name



    # def _get_time(self):
    #     request = requests.get("https://my-calend.ru/date-and-time-today")
    #     #b = bs4.BeautifulSoup(request.text, "html.parser")
    #     b = BeautifulSoup(request.text, "html.parser")
    #     return self._clean_all_tag_from_str(str(b.select(".page")[0].findAll("h2")[1])).split()[1]

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
        """ The function gets and anylizes VK user messages """
        # 0. СЕКС

        #self.dating_questionnaire.append(self._COMMANDS2[message.upper()])
        if message.upper() == self._COMMANDS[0]:
            self.dating_questionnaire.append(self._USER_ID)
            #print('***self.dating_questionnaire:', self.dating_questionnaire)
            return f"Отлично, {self._USERNAME}! Далее вам будут заданы 4 вопроса для поиска. " \
                   f"Если вам нужно прервать опрос - наберите ПРЕРВАТЬ, для продолжения - ПРОДОЛЖИТЬ. " \
                   f"Важно точно соблюдать формат и структутру ответов! " \
                   f"Вопрос №1: напишите возраст партнера ОТ. Формат ответа: ВОЗРАСТ ОТ и " \
                   f"следующим сообщением ДВУЗНАЧНОЕ число. Например: " \
                   f"ответ 1-1: ВОЗРАСТ ОТ, ответ 1-2: 18"

        # 1. ВОЗРАСТ ОТ
        elif message.upper() == self._COMMANDS[1]:
            self.answer_1_2 = True
            self.dating_questionnaire.append(0)
            print('***self.dating_questionnaire:', self.dating_questionnaire)


        # 2. ВОЗРАСТ ДО
        elif message.upper() == self._COMMANDS[2]:
            age_to = answer
            self.dating_questionnaire.append(age_to)
            print(f'Сохранен возраст до:', self.dating_questionnaire[2])
            return f"Вопрос №3: напишите пол партнера. Формат ответа: ПОЛ и " \
                   f"следующим сообщением 2 (для поиска мужчин), 1 (для поиска женщин) или 0 (для поиска мужчин и женщин). Например: " \
                   f"ответ 3-1: ПОЛ" \
                   f"ответ 3-2: 1"

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

        # *.Старт опроса
        else:
            # if self.answer_1_2:
            #     age_from = int(message)
            #     self.dating_questionnaire.append(age_from)
            #     print(f'Сохранен возраст от:', self.dating_questionnaire[1])
            #     print(f"Вопрос №2: напишите возраст партнера ДО. Формат ответа: ВОЗРАСТ ДО и "
            #           f"следующим сообщением ДВУЗНАЧНОЕ число. Например: "
            #           f"ответ 2-1: ВОЗРАСТ ДО, ответ 2-2: 25")
            #print('+++type(self._USER_ID):', type(self._USER_ID))


            # print('===result.id:', result.id, type(result))
            # print('===result.dir():', dir(result))

            #return f"Добрый день, {self._USERNAME}. Я сваха Диана приветствую вас в группе поиска большой и светлой любви! Если вы готовы начать поиск своей судьбы немедленно - напишите в ответ: секс"
            return f"Привет, {self._USERNAME}. Твой номер {self.user.id}"

dbengine = DBEngine()
dbengine.open_db_with_recreate()
users_manager_1 = UsersManager(dbengine)

# Authorization as group
vk = vk_api.VkApi(token=VK_API_KEY, api_version='5.124')

# work with messages
longpoll = VkLongPoll(vk)

def write_msg(user_id, message):
    #vk.method('messages.send', {'user_id': user_id, 'message': message,  'random_id': randrange(10 ** 7),})
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
            bot = VkBot(TOKEN_VK, event.user_id)

            write_msg(event.user_id, bot.new_message(event.text))
            #global answer
            answer = event.text
            print('Text: ', answer)
            print("-------------------")


#UsersSearch.test_message_send()
