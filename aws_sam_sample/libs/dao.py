from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.ext.declarative import declarative_base

from aws_sam_sample.libs.session import Session

Base = declarative_base()


class Member(Base):
    __tablename__ = 'members'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    laundh_at = Column(DateTime)


def find_member(id: int) -> Member:
    session = Session()
    return session.query(Member).filter_by(id=id).first()

