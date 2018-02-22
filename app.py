from os import environ as env
from typing import NamedTuple
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker


engine = create_engine(f'mysql+pymysql://root:password@{env["RDS_HOST"]}/rds')
Base = declarative_base()

Session = sessionmaker()
Session.configure(bind=engine)


class Human(Base):
    __tablename__ = 'humans'
    
    id = Column(String, primary_key=True)
    name = Column(String)


class Event(NamedTuple):
    id: int


def main(event, context): 
    e: Event = Event(**event)
    session = Session()

    human: Human = session.query(Human).filter_by(id=e.id).first()
    return {
            'id': human.id,
            'name': human.name
            }
