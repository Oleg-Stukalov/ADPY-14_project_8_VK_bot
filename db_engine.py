import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import Query, scoped_session, sessionmaker
from db_model import Base
from sqlalchemy_utils import database_exists, create_database

DB_PATH = 'postgresql://vkbot_user:vkbot@127.0.0.1:5432/ADPY-14-VKbot'

class DBEngine(object):
    session = None

    def open_db_with_recreate(self):
        engine = create_engine(DB_PATH)
        # if not database_exists(engine.url):
        #     create_database(engine.url)
        Base.metadata.drop_all(engine)
        Base.metadata.create_all(engine)
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)
        self.session = Session()


    def open_db(self):
        engine = create_engine(DB_PATH)
        Session = sessionmaker(bind=engine)
        Session.configure(bind=engine)


def test_engine_creates_db(self):
    engine = DBEngine()
    engine.init_db()
