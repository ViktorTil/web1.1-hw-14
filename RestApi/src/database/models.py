from sqlalchemy import Column, Integer, String, Date, DateTime, func, Boolean
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql.schema import ForeignKey

from src.database.db import engine

Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    phone = Column(String, unique=True, index=True)
    birthday = Column(Date)
    create_at = Column(DateTime, default=func.now())
    update_at = Column(DateTime, default=func.now(), onupdate=func.now())
    user_id = Column('user_id', ForeignKey(
        'users.id', ondelete='CASCADE'), default=None)
    user = relationship('User', backref="notes")

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    created_at = Column('crated_at', DateTime, default=func.now())
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    confirmed = Column(Boolean, default=False)
Base.metadata.create_all(bind=engine)