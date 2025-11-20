import asyncio
from utils.helper_functions import Order,Shipping_Delay,get_delivery_time,generate_tracking_id
from datetime import timedelta,datetime
from database import SessionLocal 


async def set_to_ship():
    db=SessionLocal()
   

    orders=db.query(Order).filter(Order.is_paid==True,
                                  Order.is_shipped==False,
                                  Order.is_cancelled==False).all()
    try:
        for order in orders:
            

            if(order.checkout_time+timedelta(hours=Shipping_Delay)<=datetime.utcnow()):
                
                
                order.is_shipped=True
                shipping_method=order.shipping_provider
                delta=get_delivery_time(shipping_method)

                order.estimated_delivery_date=datetime.utcnow()+timedelta(days=delta)
                order.tracking_id=generate_tracking_id()
                order.shipped_at=datetime.utcnow()

                db.add(order)
        db.commit()
        

    except Exception as e:
        print("Error running set_to_ship:", e)
        db.rollback()

    finally:
        db.close()

