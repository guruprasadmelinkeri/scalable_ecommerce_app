
from sqlalchemy import Column,Integer,Float,String,Boolean, null,DateTime,ForeignKey,Text,func
from database import Base
from datetime  import datetime,timedelta
from sqlalchemy.orm import relationship


class User(Base):
    __tablename__="products"
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String[255],nullable=False)
    description=Column(Text,nullable=False)
    price=Column(Float,nullable=False)
    stock=Column(Float,nullable=False,default=0)
    category_id=Column(Float,ForeignKey("categories.id"),nullable=False)
    image_url=Column(String[500],nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    category = relationship("Category", back_populates="products")
    cart_items = relationship("CartItem", back_populates="product", cascade="all, delete-orphan")
    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"



class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=True)

   
    products = relationship("Product", back_populates="category")

    def __repr__(self):
        return f"<Category(name='{self.name}')>"