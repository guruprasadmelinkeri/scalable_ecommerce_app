from sqlalchemy import Column,Integer,Float,String,Boolean, null,DateTime,ForeignKey,func,BOOLEAN
from database import Base
from datetime  import datetime,timedelta
from sqlalchemy.orm import relationship


class Order(Base):
    __tablename__="orders"
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey("users.id"),nullable=False)

    total_amount=Column(Float,default=0)
    is_completed=Column(Boolean,default=False)
    is_cancelled=Column(Boolean,default=False)
    completed_at=Column(DateTime,nullable=True)
    cancelled_at=Column(DateTime,nullable=True)

    created_at=Column(DateTime(timezone=True),server_default=func.now())
    updated_at=Column(DateTime(timezone=True),onupdate=func.now())
    is_paid = Column(Boolean, default=False)
    payment_method=Column(String,nullable=True)
    payment_at=Column(DateTime,nullable=True)
    payment_amount=Column(Float,nullable=True)
    

    is_shipped = Column(Boolean, default=False)
    shipped_at = Column(DateTime, nullable=True)
    delivered = Column(Boolean, default=False)
    delivered_at = Column(DateTime, nullable=True)
    shipping_provider=Column(String,nullable=True)
    tracking_id=Column(String,nullable=True)
    shipping_method=Column(String,nullable=True)
    estimated_delivery_date=Column(DateTime,nullable=True)


    user = relationship("User", back_populates="orders")


    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

    
class OrderItem(Base):
    __tablename__="order_items"
    id=Column(Integer,primary_key=True,index=True)

    order_id=Column(Integer,ForeignKey("orders.id"),nullable=False)
    product_id=Column(Integer,ForeignKey("products.id"),nullable=False)
    
    quantity=Column(Float,default=0)
    price_at_purchase=Column(Float,nullable=False)

    order = relationship("Order", back_populates="items")
    product = relationship("Product")

    def subtotal(self):
        return self.quantity * self.price_at_purchase