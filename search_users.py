from tokens import VK_ADMIN_TOKEN

class SearchParams:
    def __init__(self):
        pass

class UsersSearch:
    def __init__(self, vk):
        self.vk = vk

    def get_users(self, search_params):
        """ The function gets search_params dictionary??? and returns users list """
        users_list = []
        self.vk.method('users.search', {'sex': search_params.sex, 'status': search_params.status}) #'city': search_params.city, 'sort': 1,
        return users_list #user_list

    def search_params(self, age_min, age_max, sex=0, city, status=1):
        """ The function gets search parametres from user """
        result = self.vk.method("database.getCities", {
            'access_token': VK_ADMIN_TOKEN,
            'v': '5.77',
        })
        city_id = result['response']['items'][0].get('id')
        search_params = {
            'age_from': age_min,
            'age_to': age_max,
            'sex': sex, #1 — female; 2 — male; 0 — any
            'city': city_id,
            'status': status, #1-free
            'sort': 1, #by registaration date
            'has_photo': True,
            'v': 5.89,
            'fields': ?????????????
        }

        return search_params
