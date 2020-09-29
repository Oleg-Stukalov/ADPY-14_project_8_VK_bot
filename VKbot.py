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


#class VkBot:
class VkBot(UsersSearch):

    def __init__(self, token: str, user_id):
        self.token_VK = token
        print(f"{NL}Создан объект бота для пользователя с ID: {user_id}!") #draft for multiuser usage
        self._USER_ID = user_id
        self.user = users_manager_1.get_user(str(self._USER_ID)) #check is it known user (already there is in DB)
        if self.user == None: #if user unknown getting all external parameters from VK
            #q = UsersSearch.get_user_ext_data(UsersSearch, self._USER_ID) ###socket?????????
            q = self.get_user_ext_data(self._USER_ID) ###socket?????????
            self.user = User().with_(
                vk_id = self._USER_ID,
                first_name = q[0],
                last_name = q[1],
                age = q[2],
                age_min = q[3], #draft dating_user age_min (5 years smaller the current user)
                age_max = q[4], #draft dating_user age_max (5 years bigger the current user)
                sex = q[5], #draft dating_user sex (inversion of the current user sex)
                city = q[6], #draft dating_user city_id (same city of the current user)
                status = q[7] #draft dating_user status (1-free)
            )
            users_manager_1.save_user(self.user)
        ###BACKUP_COPY
            # if self.user == None:
            #     self.user = User().with_(vk_id=self._USER_ID)
            #     users_manager_1.save_user(self.user)

        #self._COMMANDS = ["СЕКС", "ВОЗРАСТ ОТ", "ВОЗРАСТ ДО", "ПОЛ", "ГОРОД", "ПРЕРВАТЬ", "ПРОДОЛЖИТЬ"]
        self._COMMANDS = ["?", "ВОЗРАСТ ОТ ??", "ВОЗРАСТ ДО ??", "ПОЛ ?", "ГОРОД ??", "СЕМ ПОЛОЖ ?", "+", "-", "ТОП", "-1", "-2", "-3", "-4", "-5", "-6", "-7", "-8", "-9", "-10", "ПРЕРВАТЬ"]
        self.dating_questionnaire = []
        # self.answer_1_2 = False
        # self.answer_2_2 = False
        self.dating_users = []
        self.likes_dic = {}

    def new_message(self, message):
        """ The function gets and anylizes VK user messages """
        # 0. ? (список команд)
        if message.upper() == self._COMMANDS[0]:
            pass
            return f'Список доступных команд:{NL}{NL}' \
                   f'"?" - вывести список доступных команд;{NL}{NL}' \
                   f'"ВОЗРАСТ ОТ ??" - задать нижнюю границу возраста искомого партнера, пример команды: возраст от 18;{NL}{NL}' \
                  f'"ВОЗРАСТ ДО ??" - задать верхнюю границу возраста искомого партнера, пример команды: возраст до 35;{NL}{NL}' \
                  f'"ПОЛ ?" - задать пол искомого партнера из следующих: 1 — женский, 2 — мужской, 0 — любой, пример команды: пол 1;{NL}{NL}' \
                  f'"ГОРОД *" - задать идентификатор города согласно БД Вконтакте (https://vk.com/dev/database.getCities?params[country_id]=1&params[need_all]=0&params[count]=10&params[v]=5.124), ' \
                   f'например 1 - Москва, 2 - Спб, пример команды: город 1;{NL}{NL}' \
                  f'"СЕМ ПОЛОЖ ?" - задать семейное положение искомого партнера из следующих: 1 — не женат (не замужем), 2 — встречается, 3 — помолвлен(-а), ' \
                  f'4 — женат (замужем), 5 — всё сложно, 6 — в активном поиске, 7 — влюблен(-а), 8 — в гражданском браке, пример команды: сем полож 1;{NL}{NL}' \
                  f'"+" - лайк, нравится, сохранение партнера в БД (команда доступна в режиме просмотра партнеров), пример команды: +;{NL}{NL}' \
                  f'"-" - дизлайк, не нравится, удаление партнера из БД (команда доступна в режиме просмотра партнеров), пример команды: -;{NL}{NL}' \
                  f'"ТОП" - вывести из БД список топ-10 сохраненных партнеров, пример команды: топ;{NL}{NL}' \
                  f'"-1" - удалить из списка топ-10 партнера №1 (команда доступна в режиме просмотра партнеров), пример команды: -1;{NL}{NL}' \
                  f'"-2" - удалить из списка топ-10 партнера №2 (команда доступна в режиме просмотра партнеров), пример команды: -2;{NL}{NL}' \
                  f'"-3" - удалить из списка топ-10 партнера №3 (команда доступна в режиме просмотра партнеров), пример команды: -3;{NL}{NL}' \
                  f'"-4" - удалить из списка топ-10 партнера №4 (команда доступна в режиме просмотра партнеров), пример команды: -4;{NL}{NL}' \
                  f'"-5" - удалить из списка топ-10 партнера №5 (команда доступна в режиме просмотра партнеров), пример команды: -5;{NL}{NL}' \
                  f'"-6" - удалить из списка топ-10 партнера №6 (команда доступна в режиме просмотра партнеров), пример команды: -6;{NL}{NL}' \
                  f'"-7" - удалить из списка топ-10 партнера №7 (команда доступна в режиме просмотра партнеров), пример команды: -7;{NL}{NL}' \
                  f'"-8" - удалить из списка топ-10 партнера №8 (команда доступна в режиме просмотра партнеров), пример команды: -8;{NL}{NL}' \
                  f'"-9" - удалить из списка топ-10 партнера №9 (команда доступна в режиме просмотра партнеров), пример команды: -9;{NL}{NL}, ' \
                  f'"-10" - удалить из списка топ-10 партнера №10 (команда доступна в режиме просмотра партнеров), пример команды: -10;{NL}{NL}' \
                  f'"ПРЕРВАТЬ" - временно прекратить работу с программой{NL}{NL}{NL}' \
                   f"Вопрос №1: напишите возраст партнера ОТ. Формат ответа: ВОЗРАСТ ОТ ??. Например: " \
                   f"ваш ответ: ВОЗРАСТ ОТ 18"
        # 1. ВОЗРАСТ ОТ
        elif message.upper() == self._COMMANDS[1]:
            #нарезка, выделение возраста, сохранение
            #self.dating_questionnaire.append(0)
            #print('***self.dating_questionnaire:', self.dating_questionnaire)
            #print(f'Сохранен возраст от:', self.dating_questionnaire[2])
            return f"Вопрос №2: напишите возраст партнера ДО. Формат ответа: ВОЗРАСТ ДО ??. Например: " \
                   f"ваш ответ: ВОЗРАСТ ДО 26"
        # 2. ВОЗРАСТ ДО
        elif message.upper() == self._COMMANDS[2]:
            # нарезка, выделение возраста, сохранение
            # self.dating_questionnaire.append(0)
            # print('***self.dating_questionnaire:', self.dating_questionnaire)
            # print(f'Сохранен возраст до:', self.dating_questionnaire[3])
            return f"Вопрос №3: напишите пол партнера. Формат ответа: ПОЛ ? (2 - муж, 1 - жен, 0 - любой). Например: " \
                   f"ваш ответ: ПОЛ 1"
        # 3. ПОЛ
        elif message.upper() == self._COMMANDS[3]:
            # sex = answer
            # self.dating_questionnaire.append(sex)
            # print(f'Сохранен пол:', self.dating_questionnaire[3])
            return f"Вопрос №4: напишите идентификатор города партнера ((https://vk.com/dev/database.getCities?params[country_id]=1&params[need_all]=0&params[count]=10&params[v]=5.124)," \
                   f" например 1 - Москва, 2 - Спб). Формат ответа: ГОРОД *. Например: ГОРОД 1"
        # 4. ГОРОД
        elif message.upper() == self._COMMANDS[4]:
            # city = answer
            # self.dating_questionnaire.append(city)
            # print(f'Сохранен город:', self.dating_questionnaire[4])
            return f"Вопрос №5: напишите семейное положение партнера из следующих: 1 — не женат (не замужем), 2 — встречается, 3 — помолвлен(-а), " \
                   f"4 — женат (замужем), 5 — всё сложно, 6 — в активном поиске, 7 — влюблен(-а), 8 — в гражданском браке. " \
                   f"Формат ответа: СЕМ ПОЛОЖ ?. Например: СЕМ ПОЛОЖ 1"
        # 5. СЕМ ПОЛОЖ
        elif message.upper() == self._COMMANDS[5]:
            # status = answer
            # ...
            # print(f'Сохранено семейное положение:', self.dating_questionnaire[5])
            return f"Заполнение анкеты завершено. Идет поиск подходящих партнеров. Пожалуйста, дождитесь данных по следующему партнеру в ответ напишите " \
                   f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: +"
        # 6. +
        elif message.upper() == self._COMMANDS[6]:
            #сохранение партнера в БД dating_user
            return f"Сохраняем данного партнера в БД. Пожалуйста, дождитесь данных по следующему партнеру и в ответ напишите " \
                   f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: -"
        # 7. -
        elif message.upper() == self._COMMANDS[7]:
            #сохранение партнера в БД dating_user со статусом ДИЗЛАЙК
            return f"Пропускаем данного партнера. Пожалуйста, дождитесь данных по следующему партнеру и в ответ напишите " \
                   f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: -"
        # 8. ТОП
        elif message.upper() == self._COMMANDS[8]:
            # вывод ТОП-10 СПИСКА сохраненных партнеров
            return f"Пожалуйста, дождитесь формирования и вывода списка ТОП-10. При необходимости вы можете удалить партнера из списка командой: -* (тире число)"
        # 9. -1
        elif message.upper() == self._COMMANDS[9]:
            # удаление сохраненного партнера №1
            return f"Пожалуйста, дождитесь удаления партнера."
        # 10. -2
        elif message.upper() == self._COMMANDS[10]:
            # удаление сохраненного партнера №2
            return f"Пожалуйста, дождитесь удаления партнера."
        # 11. -3
        elif message.upper() == self._COMMANDS[11]:
            # удаление сохраненного партнера №3
            return f"Пожалуйста, дождитесь удаления партнера."
        # 12. -4
        elif message.upper() == self._COMMANDS[12]:
            # удаление сохраненного партнера №4
            return f"Пожалуйста, дождитесь удаления партнера."
        # 13. -5
        elif message.upper() == self._COMMANDS[13]:
            # удаление сохраненного партнера №5
            return f"Пожалуйста, дождитесь удаления партнера."
        # 14. -6
        elif message.upper() == self._COMMANDS[14]:
            # удаление сохраненного партнера №6
            return f"Пожалуйста, дождитесь удаления партнера."
        # 15. -7
        elif message.upper() == self._COMMANDS[15]:
            # удаление сохраненного партнера №7
            return f"Пожалуйста, дождитесь удаления партнера."
        # 16. -8
        elif message.upper() == self._COMMANDS[16]:
            # удаление сохраненного партнера №8
            return f"Пожалуйста, дождитесь удаления партнера."
        # 17. -9
        elif message.upper() == self._COMMANDS[17]:
            # удаление сохраненного партнера №9
            return f"Пожалуйста, дождитесь удаления партнера."
        # 18. -10
        elif message.upper() == self._COMMANDS[18]:
            # удаление сохраненного партнера №10
            return f"Пожалуйста, дождитесь удаления партнера."
        # 19. ПРЕРВАТЬ
        elif message.upper() == self._COMMANDS[19]:
            # выход из программы
            return f"До свидания. Приходите еще!"

        # *.Старт опроса
        else:
            #return f"Привет, {self._USERNAME}. Твой номер {self.user.id}"
            return f'Добрый день. Я сваха Диана приветствую вас в группе поиска большой и светлой любви! Если вы впервые у нас, ' \
                   f'то вы можете получить список всех команд написав "?". Если вы готовы начать, то ответьте на вопрос №1 - возраст ОТ партнера. ' \
                   f'Формат ответа: ВОЗРАСТ ОТ ?? (пример: возраст от 18)'




    def test_message_send(self, vk_id=VK_SOI_ID, message='Test_message'):
        write_msg(vk_id, message)
        print('Тест сообщение отправлено на vk_id',vk_id)

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

#############BACKUP_OLD
    # def new_message(self, message):
    #     """ The function gets and anylizes VK user messages """
    #     # 0. СЕКС
    #
    #     #self.dating_questionnaire.append(self._COMMANDS2[message.upper()])
    #     if message.upper() == self._COMMANDS[0]:
    #         self.dating_questionnaire.append(self._USER_ID)
    #         #print('***self.dating_questionnaire:', self.dating_questionnaire)
    #         return f"Отлично, {self._USERNAME}! Далее вам будут заданы 4 вопроса для поиска. " \
    #                f"Если вам нужно прервать опрос - наберите ПРЕРВАТЬ, для продолжения - ПРОДОЛЖИТЬ. " \
    #                f"Важно точно соблюдать формат и структутру ответов! " \
    #                f"Вопрос №1: напишите возраст партнера ОТ. Формат ответа: ВОЗРАСТ ОТ и " \
    #                f"следующим сообщением ДВУЗНАЧНОЕ число. Например: " \
    #                f"ответ 1-1: ВОЗРАСТ ОТ, ответ 1-2: 18"
    #
    #     # 1. ВОЗРАСТ ОТ
    #     elif message.upper() == self._COMMANDS[1]:
    #         self.answer_1_2 = True
    #         self.dating_questionnaire.append(0)
    #         print('***self.dating_questionnaire:', self.dating_questionnaire)
    #
    #
    #     # 2. ВОЗРАСТ ДО
    #     elif message.upper() == self._COMMANDS[2]:
    #         age_to = answer
    #         self.dating_questionnaire.append(age_to)
    #         print(f'Сохранен возраст до:', self.dating_questionnaire[2])
    #         return f"Вопрос №3: напишите пол партнера. Формат ответа: ПОЛ и " \
    #                f"следующим сообщением 2 (для поиска мужчин), 1 (для поиска женщин) или 0 (для поиска мужчин и женщин). Например: " \
    #                f"ответ 3-1: ПОЛ" \
    #                f"ответ 3-2: 1"
    #
    #     # 3. ПОЛ
    #     elif message.upper() == self._COMMANDS[3]:
    #         sex = answer
    #         self.dating_questionnaire.append(sex)
    #         print(f'Сохранен пол:', self.dating_questionnaire[3])
    #         return f"Вопрос №4: напишите город партнера. Формат ответа: ГОРОД и " \
    #                f"следующим сообщением НАЗВАНИЕ. Например: " \
    #                f"ответ 4-1: ГОРОД" \
    #                f"ответ 4-2: Санкт-Петербург"
    #
    #     # 4. ГОРОД
    #     elif message.upper() == self._COMMANDS[4]:
    #         city = answer
    #         self.dating_questionnaire.append(city)
    #         print(f'Сохранен город:', self.dating_questionnaire[4])
    #         return f"{self._USERNAME}, усаживайтесь поудобнее - сейчас вам будут представлены лучшие партнеры!"
    #
    #     # 5. ПРЕРВАТЬ
    #     elif message.upper() == self._COMMANDS[5]:
    #         return f"До свидания, {self._USERNAME}. Скорее возвращайтесь!"
    #
    #     # 6. ПРОДОЛЖИТЬ
    #     elif message.upper() == self._COMMANDS[6]:
    #         return f"Добрый день, {self._USERNAME}! Мы с вами остановились на " \
    #                f"вопросе №{len(self.dating_questionnaire)}. Пожалуйста, для продолжения " \
    #                f"введите {self._COMMANDS[len(self.dating_questionnaire)]}"
    #
    #     # *.Старт опроса
    #     else:
    #         #return f"Привет, {self._USERNAME}. Твой номер {self.user.id}"