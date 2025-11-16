import datetime
from signal import raise_signal
from requests import session
from auth.create_tokens import create_access_token,create_refresh_token
from database import SessionLocal
from auth.auth import hash,verify
from models.user_model import RefreshToken, User
from models.cart_model import Cart
from schema.schema import CreateUser
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