
from fastapi import FastAPI,Depends,APIRouter,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import create_user,login_user
from schema.schema import CreateUser
from utils.helper_functions import get_current_user

router =APIRouter()

@router.put('/CreateUser')
def create(user:CreateUser,db:Session=Depends(get_db)):
    return create_user(user,db)

@router.put('/login')
def login(request:Request,email:str,password,db:Session=Depends(get_db)):
    return login_user(db,request,email,password,)
@router.put("/login/test")
def test_login(request:Request,db:Session=Depends(get_db)):
    
    user=get_current_user(db,request)
    return user.email
