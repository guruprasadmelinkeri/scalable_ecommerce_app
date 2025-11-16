from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import add_cartitems, create_user,login_user
from schema.schema import CartItemCreate, CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate
from utils.helper_functions import get_current_user,get_user_cart
from models.cart_model import Cart
from models.user_model import User
router =APIRouter()


@router.get("/cart")
def get_current_cart(request:Request,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return get_user_cart(request,user,db)

@router.put("/cart/additem")
def add_item_cart(request:Request,product:CartItemCreate,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return add_cartitems(request,user,product,db)