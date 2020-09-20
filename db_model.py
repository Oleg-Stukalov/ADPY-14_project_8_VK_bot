import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
import psycopg2

#################### setup ######################
Base = declarative_base()


class User(Base):
    __tablename__ = 'user'

    id = sa.Column(sa.Integer, primary_key=True)
    vk_id = sa.Column(sa.String(20), nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    second_name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    range_age = sa.Column(sa.Integer) # ??? integer >= 0 and integer <= 100
    city = sa.Column(sa.String(50))
    children = relationship('DatingUser', backref='user')


class DatingUser(Base):
    __tablename__ = 'datingUser'

    id = sa.Column(sa.Integer, primary_key=True)
    vk_id = sa.Column(sa.String(20), nullable=False)
    first_name = sa.Column(sa.String(50), nullable=False)
    second_name = sa.Column(sa.String(50), nullable=False)
    age = sa.Column(sa.Integer)  # ??? integer >= 0 and integer <= 100
    id_User = sa.Column(sa.Integer, sa.ForeignKey('User.id'))
    children = relationship('Photos', backref='datingUser')

class Photos(Base):
    __tablename__ = 'photos'

    id = sa.Column(sa.Integer, primary_key=True)
    id_DatingUser = sa.Column(sa.Integer, sa.ForeignKey('datingUser.id'))
    link_photo = sa.Column(sa.String(50))
    count_likes = sa.Column(sa.Integer)


