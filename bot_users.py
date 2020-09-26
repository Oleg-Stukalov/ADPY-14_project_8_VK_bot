from db_engine import DBEngine
import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

from db_model import Base


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    vk_id = sa.Column(sa.String(20), nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    last_name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    age_min = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    age_max = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    sex = sa.Column(sa.Integer) #0-any, 1 - female, 2 - male
    city = sa.Column(sa.Integer)
    #known_users = relationship('DatingUser', backref='user')

    def with_(self, *args, **kwargs):
        self.id = kwargs.get('id', self.id)
        self.vk_id = kwargs.get('vk_id', self.vk_id)
        self.first_name = kwargs.get('first_name', self.first_name)
        self.last_name = kwargs.get('last_name', self.last_name)
        self.age = kwargs.get('age', self.age)
        self.age_min = kwargs.get('age_min', self.age_min)
        self.age_max = kwargs.get('age_max', self.age_max)
        self.sex = kwargs.get('sex', self.sex)
        self.city = kwargs.get('city', self.city)
        return self

    def withId(self, vk_id):
        self.vk_id = vk_id
        return self

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
        self.db_engine


def test_UserManager_stores_user_well():
    print('test started')
    user_1 = User().with_(vk_id=5, sex=2, age=30, first_name='Vasia')
    print('user_1.vk_id:', user_1.vk_id)
    print('user_1.sex:', user_1.sex)
    print('user_1.age', user_1.age)
    dbengine = DBEngine()
    users_manager_1 = UsersManager(dbengine)
    users_manager_1.save_user(user_1)

    user_2 = users_manager_1.get_user(5)
    print('line___')
    print('user_2.city:', user_2.city)
    print('user_2.first_name:', user_2.first_name)
    assert(user_2.first_name == 'Vasia')

test_UserManager_stores_user_well()