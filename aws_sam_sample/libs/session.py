import threading
from os import environ as env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION = f'mysql+pymysql://root:password@{env["RDS_HOST"]}/rds?charset=utf8' if "RDS_HOST" in env else 'sqlite:///:memory:'
engine = create_engine(CONNECTION)
Session = sessionmaker()
Session.configure(bind=engine)

