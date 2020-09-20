import requests
from os.path import getsize
import json
from tokens import TOKEN_VK, VK_API_KEY, VK_SOI_ID


#CONSTANTS
OAUTH_VK_URL = 'https://oauth.vk.com/authorize'
# TOKEN_VK = '958eb5d439726565e9333aa30e50e0f937ee432e927f0dbd541c541887d919a7c56f95c04217915c32008'  # получен в Нетологии
# id_VK = input('Пожалуйста, введите id пользователя Вконтакте, копию фото которого надо сделать (при пустом вводе будет использован id552934290): ')
# id_VK = id_VK or '552934290'
# print('Сохранен id_VK: ', id_VK)

class VKUser:
    """
        VKUser is a class that do all work with VKontakte API
    """

    def __init__(self, token: str, user_id: int, params=None, headers=None):
        self.token_VK = token
        self.user_id = user_id
        self.params = params
        self.headers = headers

    def get_params(self, add_params: dict = None):
        """ The function that that prepare all params for getting VK answer """
        params = {
            'access_token': self.token_VK,
            'v': '5.77'
        }
        if add_params:
            params.update(add_params)
        return params

    def get_request(self, url, params, headers=None):
        """ The function that doing GET VK request """
        response = requests.get(url, params=params)
        return response.json()

    def put_request(self, url, params, headers):
        """ The function that doing PUT VK request """
        response = requests.put(url, params=params, headers=headers)
        return response.json()

    def get_first_name(self):
        """ The function that getting VK user first name """
        user = vk.method("users.get", {"user_ids": 1})  # вместо 1 подставляете айди нужного юзера
        first_name = user[0]['first_name']
        return first_name


    def get_second_name(self):
        """ The function that getting VK user second (last) name """
        pass

    def get_photos(self, id_VK):
        # доп параметры для скачивания фото
        photo_down_params = self.get_params(
            add_params={
                'owner_id': id_VK,
                'album_id': 'profile',
                'extended': 1
            }
        )
        response = self.get_request('https://api.vk.com/method/photos.get', photo_down_params)
        photo_url_set = set()
        # сохранение ссылок на фото
        for photo_number in range(len(response['response']['items'])):
            max_height = []
            max_width = []
            max_url = []
            for max_size in response['response']['items'][photo_number]['sizes']:
                max_height.append(max_size['height'])
                max_width.append(max_size['width'])
                max_url.append(max_size['url'])
            photo_url_set.add(max_url[max_width.index(max(max_width))])
        likes_list = []
        dates_list = []
        # имя файла по лайкам
        for likes in response['response']['items']:
            likes_list.append(likes['likes']['count'])
            dates_list.append(likes['date'])
        for index in range(1, len(likes_list)):
            if likes_list[index] == likes_list[index - 1]:
                likes_list[index] = f'{likes_list[index]}-{dates_list[index]}'
        print(f'Будем сохранять {len(photo_url_set)} следующих фото: {photo_url_set}')

        json_output = []
        files_for_upload = []
        for number, photo in enumerate(photo_url_set):
            response_img = requests.get(photo)
            with open(f'{likes_list[number]}.jpg', 'wb') as f:
                f.write(response_img.content)
                # создание JSON-отчета
                temp_dic = {'file_name': likes_list[number], 'size': getsize(f'{likes_list[number]}.jpg')}
                json_output.append(temp_dic)
                files_for_upload.append(f'{likes_list[number]}.jpg')
            print(f'Успешно скачан файл {likes_list[number]}.jpg по ссылке: {photo}')
            # сохраняю в json
            with open('output.json', 'w', encoding='utf-8') as f:
                f.write(json.dumps(json_output, ensure_ascii=False))
        print('Успешно сохранен лог файл: output.json')
        return files_for_upload