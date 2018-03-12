from typing import Any

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.ext.declarative import declarative_base

from aws_sam_sample.session import Session

Base: Any = declarative_base()


class Member(Base):
    __tablename__ = 'members'

    id = Column(String, primary_key=True)
    name = Column(String)
    age = Column(Integer)


class Project(Base):
    __tablename__ = 'projects'

    id = Column(String, primary_key=True)
    name = Column(String)
    laundh_at = Column(DateTime)


def find_member(id: str) -> Member:
    session = Session()
    return session.query(Member).filter_by(id=id).first()
