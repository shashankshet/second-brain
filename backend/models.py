# models.py

from sqlalchemy import Column,Integer,String,Text
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column,Integer,String,Text,DateTime
from datetime import datetime
from sqlalchemy import Column,Integer,String,Text,DateTime
from datetime import datetime

Base = declarative_base()

class Memory(Base):
    __tablename__ = "memories"

    id = Column(Integer, primary_key=True)

    category = Column(String)

    content = Column(Text)

    confidence = Column(Integer, default=100)

class Conversation(Base):
    __tablename__ = "conversations"

    id = Column(Integer, primary_key=True)

    role = Column(String)

    message = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )

class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id = Column(Integer, primary_key=True)

    summary = Column(Text)

    created_at = Column(
        DateTime,
        default=datetime.utcnow
    )