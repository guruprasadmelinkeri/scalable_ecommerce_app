from sqlalchemy import Column,Integer,Float,String,Boolean, null,DateTime,ForeignKey
from database import Base
from datetime  import datetime,timedelta
from sqlalchemy.orm import relationship

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String,unique=True,nullable=False)
    email=Column(String,unique=True,nullable=False)
    hashed_password=Column(String,nullable=False)
    current_token=Column(String,nullable=True)
    refresh_tokens = relationship("RefreshToken", back_populates="user", cascade="all, delete")
    cart = relationship("Cart", back_populates="user",uselist=False)
class RefreshToken(Base):
    __tablename__="refresh_tokens"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    token=Column(String,nullable=False)
    isRevoked=Column(Boolean,default=False)
    expires_at=Column(DateTime,nullable=False)
    user = relationship("User", back_populates="refresh_tokens")

