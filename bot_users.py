from db_engine import DBEngine
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

from db_model import Base, User, DatingUser, Photos


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
        user1 = User()
        user1.vk_id = vk_id
        user1.city = 'spb'
        return user1

    def save_user(self, user):
        sa.session.add(user)
        sa.session.commit()


def test_UserManager_stores_user_well():
    print('test started')
    user_1 = User().with_(vk_id=5, sex=2, age=30, first_name='Vasia')
    print('user_1.vk_id:', user_1.vk_id)
    print('user_1.sex:', user_1.sex)
    print('user_1.age', user_1.age)
    dbengine = DBEngine()
    dbengine.open_db_with_recreate()
    users_manager_1 = UsersManager(dbengine)
    users_manager_1.save_user(user_1)

    user_2 = users_manager_1.get_user(5)
    print('line___')
    print('user_2.city:', user_2.city)
    print('user_2.first_name:', user_2.first_name)
    assert(user_2.first_name == 'Vasia')

test_UserManager_stores_user_well()