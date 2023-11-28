import configparser
import pathlib
from fastapi import HTTPException, status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from src.conf.config import settings

SQLALCHEMY_DATABASE_URL = settings.sqlalchemy_database_url
#engine = create_engine(SQLALCHEMY_DATABASE_URL)
engine = create_engine("sqlite:///mycontacts.db")
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=str(err))
    finally:
        db.close()


'''
file_config = pathlib.Path(__file__).parent.parent.joinpath('conf/config.ini')
config = configparser.ConfigParser()
config.read(file_config)

username = config.get('DB', 'USER')
password = config.get('DB', 'PASSWORD')
database_name = config.get('DB', 'DB_NAME')
domain = config.get('DB', 'DOMAIN')
port = config.get('DB', 'PORT')

URI = f'postgresql://{username}:{password}@{domain}:{port}/{database_name}'

#engine = create_engine(URI, echo = False)
engine = create_engine("sqlite:///mycontacts.db")
DBSession = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = DBSession()
    try:
        yield db   
    except SQLAlchemyError as err:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail =str(err))
    finally:
        db.close()'''
        


    
