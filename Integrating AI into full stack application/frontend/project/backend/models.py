from sqlalchemy import Column,Integer,String,Text,DateTime,Float
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime

Base = declarative_base()

class ChatLog(Base):
    """Database model to store the chat session logs."""

    __tablename__ = "chat_logs"

    id = Column(Integer,primary_key=True,index=True)
    user_id = Column(String(255),index=True,nullable=False)
    prompt=Column(Text,nullable=False)
    response = Column(Text,nullable=False)
    tokens = Column(Integer,nullable=False)
    sentiment = Column(Float,nullable=False)
    created_at = Column(DateTime,default=datetime.utcnow,nullable=False)

    def __repr__(self): 
        """String representation of the chatLog model"""
        return f"<ChatLog(id={self.id},user_id='{self.user_id}',tokens={self.tokens})>"