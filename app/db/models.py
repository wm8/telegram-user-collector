from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    phone = Column(String)
    # ... другие поля

class Channel(Base):
    __tablename__ = 'channels'
    id = Column(BigInteger, primary_key=True)
    username = Column(String)
    title = Column(String)
    description = Column(String)
    subscriptions = Column(Integer)
    # ... другие поля

class Media:
    __tablename__ = 'media'
    id = Column(BigInteger, primary_key=True)
    url = Column(String)

class Message(Base):
    __tablename__ = 'messages'
    id = Column(BigInteger, primary_key=True)
    mid = Column(BigInteger, index=True)
    channel_id = Column(BigInteger, ForeignKey('channels.id'), index=True)
    text = Column(String)
    date = Column(DateTime)

class Comment(Base):
    __tablename__ = 'comments'
    id = Column(BigInteger, primary_key=True)
    mid = Column(BigInteger, ForeignKey('messages.mid'))
    channel_id = Column(BigInteger, ForeignKey('channels.id'))
    text = Column(String)
    date = Column(DateTime)

