from os import environ as env

from sqlalchemy import Column, String
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

engine = create_engine(f'mysql+pymysql://root:password@{env["RDS_HOST"]}/rds')
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)


class Human(Base):
    __tablename__ = 'humans'
    
    id = Column(String, primary_key=True)
    name = Column(String)


def find_human(id: int) -> Human:
    session = Session()
    return session.query(Human).filter_by(id=id).first()

