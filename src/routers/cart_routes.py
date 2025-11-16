from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import create_user,login_user
from schema.schema import CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate
from utils.helper_functions import get_current_user,get_user_cart
from models.cart_model import Cart
from models.user_model import User
router =APIRouter()


@router.get("/cart")
def get_current_cart(request:Request,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return get_user_cart(request,user,db)
