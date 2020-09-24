class SearchParams:
    def __init__(self):
        pass

class UsersSearch:
    def __init__(self, vk):
        self.vk = vk

    def get_users(self, search_params): #приним SearchParams, возвращ список польз
        users_list = []
        self.vk.method('users.search', {'sex': search_params.sex, 'status': search_params.status}) #'city': search_params.city, 'sort': 1,
        return users_list #user_list
