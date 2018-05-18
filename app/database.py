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


def get_all_d():
    out = "distance values: "
    for instance in session.query(Distances).order_by(Distances.id):
        out = out + str(instance.value) + "; "
    return out


def add(distance_value):
    distance = Distances(value=distance_value)
    session.add(distance)
    session.commit()
    return "distance value added to DB"


# database schemas
class Distances(Base):
    __tablename__ = 'distances_table'

    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
