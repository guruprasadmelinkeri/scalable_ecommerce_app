import string,random
import datetime
from requests import session
from auth.create_tokens import create_access_token,create_refresh_token
from database import SessionLocal
from auth.auth import hash,verify
from models.order_model import Order, OrderItem
from models.product_model import Product
from models.user_model import RefreshToken, User
from models.cart_model import Cart, CartItem
from schema.schema import CartItemCreate, CartItemDelete, CartItemUpdate, CreateUser, DeliveryRequest, PaymentRequest, ShippingRequest
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request
from datetime import datetime,timedelta

from auth.create_tokens import ALGORITHM,SECRET_KEY,jwt
from jose import JWTError,jwt

def create_user(user:CreateUser,db=Session):
    """funtion used for creating a user """
    new_user=db.query(User).filter(User.email==user.email or User.username==user.username).first()
    if new_user:
        raise HTTPException(status_code=400,detail="email taken")
    new_user=User(
        email=user.email,
        hashed_password=hash(user.password),
        username=user.username

    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return { f"username:{new_user.username},email:{new_user.email}"}



    
def login_user(db:Session,request:Request,email:str,password=str):
    """ function to authenticate user and get the tokens """

    user=db.query(User).filter(User.email==email).first()
    if not user or not verify(password,user.hashed_password):
        raise HTTPException(status_code=400,detail="wrong credentials")
    access_token=create_access_token({"sub":email},timedelta(minutes=60))
    refresh_token=create_refresh_token({"sub":email},timedelta(days=7))

    new_tokens=RefreshToken(
        token=refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow()+timedelta(days=7)
    )
    db.add(new_tokens)
    db.add(user)
    db.commit()

    request.session["access_token"]=access_token
    

    return {"user authenticated"}
    
def refresh_access_tokens(request:Request,db:Session,user_id,email:str):
    """function to refresh the access token and rotate the refresh token and will return the user """
    
    user=db.query(User).filter(User.email==email).first()

    check_refresh_token=db.query(RefreshToken).filter(RefreshToken.user_id==user_id,
                                                    RefreshToken.isRevoked==False,
                                                    RefreshToken.expires_at > datetime.utcnow(),
                                                    ).order_by(RefreshToken.id.desc()).first()



    if not check_refresh_token or (check_refresh_token.isRevoked):
        raise HTTPException(status_code=400,detail="please login again")
    
    check_refresh_token.isRevoked=True
    new_access_token=create_access_token({"sub":email},timedelta(minutes=60))
    new_refresh_token=create_refresh_token({"sub":email},timedelta(days=7))

    new_tokens=RefreshToken(
        token=new_refresh_token,
        user_id=user.id,
        expires_at=datetime.utcnow()+timedelta(days=7)
    )
    request.session["access_token"]=new_access_token

    db.add(user)
    db.add(new_tokens)
    db.commit()
    return user








def get_current_user(db:Session,request:Request):
    '''Function to validate the user and the user cookies stored[the access tokens ]'''
    credential_error = HTTPException(status_code=401, detail="Couldn't verify credentials")
    token=request.session.get("access_token")
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM)
        email=payload.get("sub")
        if not email:
            raise HTTPException(status_code=404,detail="Inavalid User")
        user=db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=404,detail="Inavalid User")
        return user

    

    

    except jwt.ExpiredSignatureError:
        payload=jwt.decode(token,SECRET_KEY,algorithms=ALGORITHM,options={"verify_exp": False})
        email=payload.get("sub")
        user=db.query(User).filter(User.email==email).first()
        if not user:
            raise HTTPException(status_code=404,detail="Inavalid User")
        
        new_user=refresh_access_tokens(request,db,user.id,email)
        if not new_user:
            raise HTTPException(status_code=404,detail="Login again")
        return new_user
    



    except JWTError:
    
            raise credential_error
    

def get_all_users(request:Request,db:Session):
    users=db.query(User).all()

    return users



## get user cart
def get_user_cart(request:Request,user:User,db:Session):
    """ used for retriving the user cart"""
   
    
    cart=db.query(Cart).filter(Cart.user_id==user.id).first()
    if not cart:
        cart=Cart(
            user_id=user.id
        )
        db.add(cart)
        db.commit()
        db.refresh(cart)
    return cart

## add cartitems to cart

def add_cartitems(request:Request,user:User,product:CartItemCreate,db:Session):
    """ method used for adding new items or increasing quantity of items"""

    cart=get_user_cart(request,user,db)
    new_product=db.query(Product).filter(Product.id==product.product_id).first()
    
    if(product.quantity<0):
        raise HTTPException(status_code=400,detail="Enter positive quantity")
    
    if ( not new_product):
        raise HTTPException(status_code=400,detail="Product not found")
    
    if (product.quantity>new_product.stock):
        raise HTTPException(status_code=400,detail="Items out of stock")
    


    cart_item=db.query(CartItem).filter(CartItem.cart_id==cart.id,
                                       CartItem.product_id==new_product.id).first()
    
    if not cart_item:
        cart_item=CartItem(
            cart_id=cart.id,
            product_id=new_product.id,
            quantity=product.quantity,
            price_at_addition=new_product.price,
        )
        db.add(cart)
        db.add(cart_item)
        db.commit()
        db.refresh(cart_item)
        db.refresh(cart)
        return cart.items
        

    
    
    cart_item.quantity+=product.quantity
    cart_item.price_at_addition=new_product.price

   
    
    db.add(cart)
    db.add(cart_item)
    db.commit()
    db.refresh(cart_item)
    db.refresh(cart)
    return cart.items
    
def modify_cartitems(request:Request,user:User,update:CartItemUpdate,db:Session):
    """ used for updating cartitem qauntity"""
    cart=get_user_cart(request,user,db)
    cart_item=db.query(CartItem).filter(CartItem.cart_id==cart.id,
                                        CartItem.product_id==update.product_id).first()
    product=db.query(Product).filter(Product.id==update.product_id).first()
    
    if not cart_item:
        raise HTTPException(status_code=400,detail="Product not found")
    
    if(update.quantity<0):
        raise HTTPException(status_code=400,detail="Enter positive quantity")
    
    if ( not product):
        raise HTTPException(status_code=400,detail="Product not found")
    
    if (update.quantity>product.stock):
        raise HTTPException(status_code=400,detail="Items out of stock")
    
    
    if (update.quantity==0):
        cart_item.quantity=update.quantity
        db.delete(cart_item)
        db.add(cart)
        db.commit()
        db.refresh(cart)
        return cart.total_cost()
    
    cart_item.quantity=update.quantity

    
    db.commit()
    db.refresh(cart)
    

    return cart.total_cost()
    


def delete_cart_item(request:Request,user:User,update:CartItemDelete,db:Session):
    cart=get_user_cart(request,user,db)
    product=db.query(Product).filter(Product.id==update.product_id).first()
    if not product:
        raise HTTPException(status_code=404,detail="product not found")
    
    cart_item=db.query(CartItem).filter(CartItem.product_id==update.product_id,
                                        CartItem.cart_id==cart.id).first()
    
    if not cart_item:
        
        raise HTTPException(status_code=404,detail="product not found in cart")
    
    db.delete(cart_item)
    db.commit()
    
    return {"cart_total":cart.total_cost()}

def clear_cart(request:Request,user:User,db:Session):
    cart=get_user_cart(request,user,db)
    items=db.query(CartItem).filter(CartItem.cart_id==cart.id).all()
    for item in items:
        db.delete(item)
        db.commit()
    
    return cart.total_cost()




###cart checkout and order methods 




def complete_order(request:Request,user:User,db:Session):
    cart=get_user_cart(request,user,db)
    
    cart_items=db.query(CartItem).filter(CartItem.cart_id==cart.id).all()

    if not cart_items or (cart.total_cost() == 0):
        raise HTTPException(status_code=400,detail="cart is empty cant proceed ")
    for item in cart_items:
        curr_product=db.query(Product).filter(Product.id==item.product_id).first()
        if(item.quantity>curr_product.stock):
            raise HTTPException(status_code=400,detail=f"only {curr_product.stock} items of {curr_product.name} left ")
        
    
    try:
        order=Order(

            user_id=user.id,
                )
        db.add(order)
        db.flush()
        total=0

        for item in cart_items:
            curr_product=db.query(Product).filter(Product.id==item.product_id).first()
            order_item=OrderItem(
                order_id=order.id,
                product_id=item.product_id,
                quantity=item.quantity,
                price_at_purchase=curr_product.price
            )

            db.add(order_item)
            if(item.quantity>curr_product.stock):
                raise HTTPException(status_code=400,detail=f"only {curr_product.stock} items of {curr_product.name} left ")
            curr_product.stock-=item.quantity
            
            db.add(curr_product)
            total+=order_item.subtotal()

        order.total_amount=total
        cart_total=clear_cart(request,user,db)
        
        db.add(order)
        db.add(cart)
        db.commit()
        db.refresh(cart)

        return {"order_id":order.id,"items":order.items,"total":order.total_amount,"status":order.is_completed}
    

        



    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")

def get_order_history(request:Request,user:User,db:Session):
    orders=db.query(Order).filter(Order.user_id==user.id).all()
    

    if not orders:
        raise HTTPException(status_code=404,detail="no orders to display")
    
    return orders



def order_cancel(request:Request,user:User,order_id:int,db:Session):
    order=db.query(Order).filter(Order.id==order_id).first()
    if not order:
        raise HTTPException(status_code=400,detail="Order not found")
    
    if order.is_cancelled or (order.is_completed) or order.is_shipped :
        raise HTTPException(status_code=400,detail="cant cancel order")
    try:
        items=db.query(OrderItem).filter(OrderItem.order_id==order_id).all()
        for item in items:
            product=db.query(Product).filter(Product.id==item.product_id).first()
            product.stock+=item.quantity
            db.add(product)
            
        order.is_cancelled=True
        db.commit()
        return order.items
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Order creation failed: {str(e)}")
    



    ##payment shipping and delivcery methods

def complete_payment(request:Request,user:User,payload:PaymentRequest,db:Session):
    order=db.query(Order).filter(Order.user_id==user.id,
                                 Order.id==payload.order_id).first()
    
    if not order:
        raise HTTPException(status_code=400,detail="order not found please check credentials")
    if order.is_cancelled or order.is_completed or order.is_paid or order.is_shipped:
        raise HTTPException(status_code=400,detail="cant process payment")
    order_amoont=order.total_amount

    order.is_paid=True
    order.payment_at=datetime.now()
    order.payment_method=payload.payment_method

    db.add(order)
    db.commit()

    return {"order_id":order.id,"status":"paid"}

def generate_tracking_id():
    rand = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
    return f"SHIP-{rand}"



###
shipping_methods={
    "Express":2,
    "Fast":5,
    "Standard":10
}


def get_delivery_time(method:string):
    '''for no of delivery days'''
    if not method in shipping_methods:
        raise HTTPException(status_code=400,detail="not valid order provider")
    return shipping_methods[method]

def start_shipping(request:Request,user:User,payload:ShippingRequest,db:Session):

    order=db.query(Order).filter(Order.user_id==user.id,
                                 Order.id==payload.order_id).first()
    if not order:
        raise HTTPException(status_code=400,detail="order not found please check credentials")
    if order.is_cancelled or order.is_completed or (not order.is_paid) or order.is_shipped or order.delivered:
        raise HTTPException(status_code=400,detail="cant process shipping")
    
    order.is_shipped=True

    delta=get_delivery_time(payload.shipping_method)

    order.estimated_delivery_date=datetime.utcnow()+timedelta(days=delta)
    order.tracking_id=generate_tracking_id()
    order.shipped_at=datetime.now()

    db.add(order)
    db.commit()

    
    return {"order_id":order.id,"status":"shipped","shipping_method":payload.shipping_method ,"estimated delivery date":order.estimated_delivery_date}




def complete_delivery(request:Request,user:User,payload:DeliveryRequest,db:Session):
    order=db.query(Order).filter(Order.user_id==user.id,
                                Order.id==payload.order_id).first()
    if not order:
        raise HTTPException(status_code=400,detail="order not found please check credentials")
    
    if order.is_cancelled or order.is_completed or (not order.is_paid) or (not order.is_shipped) or order.delivered:
        raise HTTPException(status_code=400,detail="cant process delivery")
    
    order.delivered=True
    order.delivered_at=datetime.now()
    order.is_completed=True
    order.completed_at=datetime.now()

    db.add(order)
    db.commit()

    return {"order_id":order.id,"status":"deliverd","delivery_method":payload.delivery_method}
