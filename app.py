from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://root:password@localhost/rds', echo=True)
Base = declarative_base()


class Human(Base):
    __tablename__ = 'humans'
    
    id = Column(String, primary_key=True)
    name = Column(String)


Session = sessionmaker()
Session.configure(bind=engine)


def main(event, context): 
    session = Session()

    for instance in session.query(Human).order_by(Human.id):
        print(instance.name)
    return {'ping': 'ok'}

