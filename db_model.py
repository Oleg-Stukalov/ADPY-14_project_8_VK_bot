import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

#################### setup ######################
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    vk_id = sa.Column(sa.String(20), unique=True, nullable=False)
    first_name = sa.Column(sa.String(50))
    last_name = sa.Column(sa.String(50))
    age = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    age_min = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    age_max = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    sex = sa.Column(sa.Integer) #0-any, 1 - female, 2 - male
    city = sa.Column(sa.Integer)
    children = relationship('DatingUser', backref='user')

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

class DatingUser(Base):
    __tablename__ = 'datingUser'

    id = sa.Column(sa.Integer, primary_key=True)
    vk_id = sa.Column(sa.String(20), unique=True, nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    last_name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer)  # ??? integer >= 0 and integer <= 100
    id_User = sa.Column(sa.Integer, sa.ForeignKey('user.id'))
    photos = relationship('Photos', backref='datingUser')

class Photos(Base):
    __tablename__ = 'photos'

    id = sa.Column(sa.Integer, primary_key=True)
    id_DatingUser = sa.Column(sa.Integer, sa.ForeignKey('datingUser.id'))
    url = sa.Column(sa.String(50))
    likes_count = sa.Column(sa.Integer)


