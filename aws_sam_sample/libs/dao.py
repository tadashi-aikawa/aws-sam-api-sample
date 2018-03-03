from sqlalchemy import Column, String, Integer
from sqlalchemy.ext.declarative import declarative_base

from aws_sam_sample.libs.session import Session

Base = declarative_base()


class Human(Base):
    __tablename__ = 'humans'

    id = Column(Integer, primary_key=True)
    name = Column(String)


def find_human(id: int) -> Human:
    session = Session()
    return session.query(Human).filter_by(id=id).first()

