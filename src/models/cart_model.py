from sqlalchemy import Column,Integer,Float,String,Boolean, null,DateTime,ForeignKey,func
from database import Base
from datetime  import datetime,timedelta
from sqlalchemy.orm import relationship

class Cart(Base):
    __tablename__="carts"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    user = relationship("User", back_populates="cart")
    items = relationship("CartItem", back_populates="cart", cascade="all, delete-orphan")
    def total_cost(self):
        return sum(item.subtotal() for item in self.items) if self.items else 0   
    
class CartItem(Base):
    __tablename__ = "cart_items"

    id = Column(Integer, primary_key=True, index=True)
    cart_id = Column(Integer, ForeignKey("carts.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False, default=1)
    price_at_addition = Column(Float, nullable=False)  
    cart = relationship("Cart", back_populates="items")
    product = relationship("Product")

    def subtotal(self):
        return self.quantity * self.price_at_addition


