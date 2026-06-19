# models.py

from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)

    category = Column(String)
    content = Column(Text)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)
    role = Column(String)
    message = Column(Text)