from db_engine import DBEngine


class BotUser: #left side user
    first_name = None
    last_name = None
    age = None
    age_min = None
    age_max = None
    sex = None
    city = None

    def __init__(self, vk_id):
        self.vk_id = vk_id


class UsersManager:
    first_name = None
    last_name = None
    age = None
    age_min = None
    age_max = None
    sex = None
    city = None

    def __init__(self, db_engine):
        self.db_engine = db_engine

    def get_user(self, vk_id):
        user1 = BotUser(vk_id=vk_id)
        user1.city = 'spb'
        return user1

    def save_user(self, user):
        self.db_engine


def test_UserManager_stores_user_well():
    print('test started')
    user_1 = BotUser(5)
    dbengine = DBEngine()
    users_manager_1 = UsersManager(dbengine)
    user_1.first_name = 'Vasia'
    users_manager_1.save_user(user_1)

    user_2 = users_manager_1.get_user(5)
    print('line___')
    print('user_2.city:', user_2.city)
    print('user_2.first_name:', user_2.first_name)
    assert(user_2.first_name == 'Vasia')

test_UserManager_stores_user_well()