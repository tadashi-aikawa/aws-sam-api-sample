import threading
from os import environ as env

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SessionManager:
    _instance = None
    _lock = threading.Lock()
    Session = None

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
                    engine = create_engine(f'mysql+pymysql://root:password@{env["RDS_HOST"]}/rds')
                    cls._instance.Session = sessionmaker()
                    cls._instance.Session.configure(bind=engine)

        return cls._instance

    @classmethod
    def create(cls):
        return cls._get().Session()
