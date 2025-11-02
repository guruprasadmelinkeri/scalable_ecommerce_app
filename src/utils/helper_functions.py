from requests import session
from auth.create_tokens import create_access_token
from database import SessionLocal
from auth.auth import hash,verify
from models.user_model import User
from schema.schema import CreateUser
from sqlalchemy.orm import Session
from fastapi import HTTPException,Request
from datetime import timedelta
from auth.create_tokens import ALGORITHM,SECRET_KEY,jwt
from jose import JWTError

def create_user(user:CreateUser,db=Session):
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
    user=db.query(User).filter(User.email==email).first()
    if not user or not verify(password,user.hashed_password):
        raise HTTPException(status_code=400,detail="wrong credentials")
    access_token=create_access_token({"sub":email},timedelta(minutes=60))
    db.add(user)
    db.commit()

    request.session["email"]=email
    request.session["access_token"]=access_token
    

    return {"acess token":access_token}
    

def get_current_user(db:Session,request:Request):
    credential_error = HTTPException(status_code=401, detail="Couldn't verify credentials")
    
    email=request.session.get("email")
    token=request.session.get("access_token")
    try:
        payload=jwt.decode(token,SECRET_KEY,ALGORITHM)
        if email==payload.get("sub"):
            return email

    

    except JWTError:
   
        raise credential_error

