from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from datetime import date
import requests
from users_manager import UsersManager
from db_engine import DBEngine
from db_model import User, DatingUser
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
        self._COMMAND_QUESTION = "?"
        self._COMMAND_AGE_MIN = "ВОЗРАСТ ОТ"
        self._COMMAND_AGE_MAX ="ВОЗРАСТ ДО"
        self._COMMAND_SEX = "ПОЛ"
        self._COMMAND_CITY = "ГОРОД"
        self._COMMAND_STATUS = "СЕМ ПОЛОЖ"
        self._COMMAND_TOP = "ТОП"
        self._COMMAND_NEG_NUMBER = "-"
        self._COMMAND_POS_NUMBER = "+"
        self._COMMAND_INTERRUPTION = "ПРЕРВАТЬ"
        self.dating_questionnaire = []
        # self.answer_1_2 = False
        # self.answer_2_2 = False
        self.dating_users = [] #list of vk_id of searched dating_users
        self.likes_dic = {}

    def new_message(self, message):
        """ The function gets and anylizes VK user messages """
        # ? (список команд)
        if message.upper().startswith(self._COMMAND_QUESTION):
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
        # ВОЗРАСТ ОТ
        elif message.upper().startswith(self._COMMAND_AGE_MIN):
            #нарезка, выделение возраста, сохранение
            message_split = message.upper().split(' ')
            if len(message_split) == 3:
                self.user.age_min = int(message_split[-1])
            print(f'Сохранен возраст от:', self.user.age_min)
            return f"Вопрос №2: напишите возраст партнера ДО. Формат ответа: ВОЗРАСТ ДО ??. Например: " \
                   f"ваш ответ: ВОЗРАСТ ДО 26"
        # ВОЗРАСТ ДО
        elif message.upper().startswith(self._COMMAND_AGE_MAX):
            # нарезка, выделение возраста, сохранение
            message_split = message.upper().split(' ')
            if len(message_split) == 3:
                self.user.age_max = int(message_split[-1])
            print(f'Сохранен возраст до:', self.user.age_max)
            return f"Вопрос №3: напишите пол партнера. Формат ответа: ПОЛ ? (2 - муж, 1 - жен, 0 - любой). Например: " \
                   f"ваш ответ: ПОЛ 1"
        # ПОЛ
        elif message.upper().startswith(self._COMMAND_SEX):
            message_split = message.upper().split(' ')
            if len(message_split) == 2:
                self.user.sex = int(message_split[-1])
            print(f'Сохранен идентификатор пола:', self.user.sex)
            return f"Вопрос №4: напишите идентификатор города партнера ((https://vk.com/dev/database.getCities?params[country_id]=1&params[need_all]=0&params[count]=10&params[v]=5.124)," \
                   f" например 1 - Москва, 2 - Спб). Формат ответа: ГОРОД *. Например: ГОРОД 1"
        # ГОРОД
        elif message.upper().startswith(self._COMMAND_CITY):
            message_split = message.upper().split(' ')
            if len(message_split) == 2:
                self.user.city = int(message_split[-1])
            print(f'Сохранен идентификатор города:', self.user.city)
            return f"Вопрос №5: напишите семейное положение партнера из следующих: 1 — не женат (не замужем), 2 — встречается, 3 — помолвлен(-а), " \
                   f"4 — женат (замужем), 5 — всё сложно, 6 — в активном поиске, 7 — влюблен(-а), 8 — в гражданском браке. " \
                   f"Формат ответа: СЕМ ПОЛОЖ ?. Например: СЕМ ПОЛОЖ 1"
        # СЕМ ПОЛОЖ
        elif message.upper().startswith(self._COMMAND_STATUS):
            message_split = message.upper().split(' ')
            if len(message_split) == 3:
                self.user.status = int(message_split[-1])
            print(f'Сохранен статус семейного положения:', self.user.age_min)
            #getting dating_users vk_id list
            self.dating_users = self.get_users(self.search_params(self.user.age_min, self.user.age_max, self.user.city, self.user.sex, self.user.status))

            for vk_id in self.dating_users:
                q = self.get_user_ext_data(vk_id)
                self.datinguser = DatingUser().with_(
                    vk_id=vk_id,
                    first_name=q[0],
                    last_name=q[1],
                    age=q[2],
                    id_User=self._USER_ID
                )
                users_manager_1.save_dating_user(self.datinguser)


            #get 3 photos of each dating_user



            #show 3 photos of each dating_user

            return f"Заполнение анкеты завершено. Идет поиск подходящих партнеров. Пожалуйста, дождитесь данных по следующему партнеру в ответ напишите " \
                   f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: +"
            # return [f"Заполнение анкеты завершено. Идет поиск подходящих партнеров. Пожалуйста, дождитесь данных по следующему партнеру в ответ напишите " \
            #        f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: +", SEARCH_RESULT]

        # # +
        # elif message.upper().startswith(self._COMMAND_PLUS):
        #     #сохранение партнера в БД dating_user
        #     return f"Сохраняем данного партнера в БД. Пожалуйста, дождитесь данных по следующему партнеру и в ответ напишите " \
        #            f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: -"
        # # -
        # elif message.upper().startswith(self._COMMAND_MINUS):
        #     #сохранение партнера в БД dating_user со статусом ДИЗЛАЙК
        #     return f"Пропускаем данного партнера. Пожалуйста, дождитесь данных по следующему партнеру и в ответ напишите " \
        #            f"+ (нравится) или - (не нравится). Формат ответа: + или -. Например: -"

        # ТОП
        elif message.upper().startswith(self._COMMAND_TOP):
            # вывод ТОП-10 СПИСКА сохраненных партнеров
            return f"Пожалуйста, дождитесь формирования и вывода списка ТОП-10. При необходимости вы можете удалить партнера из списка командой: -* (тире число)"
        # -*
        elif message.upper().startswith(self._COMMAND_NEG_NUMBER):

            # -1
            if message.upper() == '-1':
                # удаление сохраненного партнера №1
                self.dating_users[0] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -2
            elif message.upper() == '-2':
                # удаление сохраненного партнера №2
                self.dating_users[1] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -3
            elif message.upper() == '-3':
                # удаление сохраненного партнера №3
                self.dating_users[2] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -4
            elif message.upper() == '-4':
                # удаление сохраненного партнера №4
                self.dating_users[3] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -5
            elif message.upper() == '-5':
                # удаление сохраненного партнера №5
                self.dating_users[4] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -6
            elif message.upper() == '-6':
                # удаление сохраненного партнера №6
                self.dating_users[5] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -7
            elif message.upper() == '-7':
                # удаление сохраненного партнера №7
                self.dating_users[6] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -8
            elif message.upper() == '-8':
                # удаление сохраненного партнера №8
                self.dating_users[7] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -9
            elif message.upper() == '-9':
                # удаление сохраненного партнера №9
                self.dating_users[8] = None
                return f"Пожалуйста, дождитесь удаления партнера."
            # -10
            elif message.upper() == '-10':
                # удаление сохраненного партнера №10
                self.dating_users[9] = None
                return f"Пожалуйста, дождитесь удаления партнера." # -*
        # +*
        elif message.upper().startswith(self._COMMAND_POS_NUMBER):

            # +1
            if message.upper() == '+1':
                # сохраненение партнера №1
                #datingUSER
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +2
            elif message.upper() == '+2':
                # сохраненение партнера №2
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +3
            elif message.upper() == '+3':
                # сохраненение партнера №3
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +4
            elif message.upper() == '+4':
                # сохраненение партнера №4
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +5
            elif message.upper() == '+5':
                # сохраненение партнера №5
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +6
            elif message.upper() == '+6':
                # сохраненение партнера №6
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +7
            elif message.upper() == '+7':
                # сохраненение партнера №7
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +8
            elif message.upper() == '+8':
                # сохраненение партнера №8
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +9
            elif message.upper() == '+9':
                # сохраненение партнера №9
                return f"Пожалуйста, дождитесь сохранения партнера."
            # +10
            elif message.upper() == '+10':
                # сохраненение партнера №10
                return f"Пожалуйста, дождитесь сохранения партнера."

        # ПРЕРВАТЬ
        elif message.upper().startswith(self._COMMAND_INTERRUPTION):
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