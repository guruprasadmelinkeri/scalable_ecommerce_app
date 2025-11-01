from fastapi import FastAPI,Depends,APIRouter
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import create_user,login_user
from schema.schema import CreateUser

router =APIRouter()

@router.put('/CreateUser')
def create(user:CreateUser,db:Session=Depends(get_db)):
    return create_user(user,db)

@router.put('/login')
def login(email:str,password,db:Session=Depends(get_db)):
    return login_user(email,password,db)