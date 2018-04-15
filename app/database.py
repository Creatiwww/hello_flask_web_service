import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import Column, Integer, String

user = os.environ['POSTGRES_USER']
pwd = os.environ['POSTGRES_PASSWORD']
db = os.environ['POSTGRES_DB']
host = 'db'
port = '5432'

engine = create_engine('postgres://%s:%s@%s:%s/%s' % (user, pwd, host, port, db))
session = scoped_session(sessionmaker(autocommit=False,
                                      autoflush=False,
                                      bind=engine))
Base = declarative_base()
Base.query = session.query_property()


def init_db():
    Base.metadata.create_all(bind=engine)
    return "DB created"


def get_all():
    out = "users: "
    for instance in session.query(Users).order_by(Users.id):
        out += instance.name
    return out


def add(user_name):
    user_name = Users(name=user_name)
    session.add(user_name)
    session.commit()
    return "user was added to DB"


class Users(Base):
    __tablename__ = 'users_table'

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
