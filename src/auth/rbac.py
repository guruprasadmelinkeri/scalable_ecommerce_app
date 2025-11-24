import fastapi
from requests import Session


from database import SessionLocal
from models.user_model import User
from utils.helper_functions import hash

def require_role(user:User,*roles):
    """function to autenticate user"""
    if user.role not in roles:
        raise fastapi.HTTPException(status_code=400,detail="Access denied")
    
def create_admin(username:str,email:str,password:str):
    db=SessionLocal()
    if not email or not password:
        raise fastapi.HTTPException(status_code=400,detail="invalid credentials")
    user=User(
        email=email,
        username=username,
        hashed_password=hash(password),
        role="admin",

    )
    db.add(user)
    db.commit()
    db.close()


    