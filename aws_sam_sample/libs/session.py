import threading
from os import environ as env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

CONNECTION = f'mysql+pymysql://root:password@{env["RDS_HOST"]}/rds' if "RDS_HOST" in env else 'sqlite:///:memory:'


class SessionManager:
    _instance = None
    _lock = threading.Lock()
    Session = None
    _engine = None

    def __new__(cls):
        raise NotImplementedError('This class is singleton')

    @classmethod
    def ___new___(cls):
        return super().__new__(cls)

    @classmethod
    def _get(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = cls.___new___()
                    cls._engine = create_engine(CONNECTION)
                    cls._instance.Session = sessionmaker()
                    cls._instance.Session.configure(bind=cls._engine)

        return cls._instance

    @classmethod
    def create(cls):
        return cls._get().Session()

    @classmethod
    def engine(cls):
        return cls._get()._engine

