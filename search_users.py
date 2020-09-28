from collections import Counter
import requests
from tokens import VK_ADMIN_TOKEN

class SearchParams:
    def __init__(self):
        pass

class UsersSearch:
    def __init__(self, vk):
        self.vk = vk

    def search_params(self, age_min, age_max, sex=0, city, status=1):
        """ The function gets search parametres from user """
        result = self.vk.method("database.getCities", {
            'access_token': VK_ADMIN_TOKEN,
            'v': '5.77',
        })
        city_id = result['response']['items'][0].get('id')
        search_params = {
            'access_token': VK_ADMIN_TOKEN,
            'age_from': age_min,
            'age_to': age_max,
            'sex': sex, #1 — female; 2 — male; 0 — any
            'city': city_id,
            'status': status, #1-free
            'sort': 1, #by registaration date
            'has_photo': 1,
            'v': '5.89',
            'fields': 'bdate, photo_max_orig'
        }
        return search_params

    def get_users(self, search_params):
        """ The function gets search_params dictionary??? and returns users list """
        users_list = []
        self.vk.method('users.search', search_params)
        return users_list #user_list

    def get_3_photos(self, vk_id):
        """ The function gets 3 photos from album 'profile' """
        photos = self.vk.method("photos.get", {
        'owner_id': vk_id,
        'album_id': 'profile',
        'extended': 1
        })
        for likes in photos['response']['items']:
            self.likes_dic[likes['likes']['count']] = ['sizes'][-1]['url']
        sorted_keys = list(self.likes_dic.keys()).sort()
        top_3 = Counter(sorted_keys).most_common(3)
        photo_0_url = self.likes_dic[top_3.keys(0)]
        photo_1_url = self.likes_dic[top_3.keys(1)]
        photo_2_url = self.likes_dic[top_3.keys(2)]
        response_img_0 = requests.get(photo_0_url)
        with open(f'{vk_id}_0.jpg', 'wb') as f:
            f.write(response_img_0.content)
        response_img_1 = requests.get(photo_1_url)
        with open(f'{vk_id}_1.jpg', 'wb') as f:
            f.write(response_img_1.content)
        response_img_2 = requests.get(photo_2_url)
        with open(f'{vk_id}_2.jpg', 'wb') as f:
            f.write(response_img_1.content)

