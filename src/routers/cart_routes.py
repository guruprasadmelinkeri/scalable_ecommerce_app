from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import add_cartitems, clear_cart, complete_order, create_user, delete_cart_item,login_user, modify_cartitems
from schema.schema import CartItemCreate, CartItemDelete, CartItemUpdate, CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate
from utils.helper_functions import get_current_user,get_user_cart
from models.cart_model import Cart
from models.user_model import User
router =APIRouter()


@router.get("/cart")
def get_current_cart(request:Request,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    cart= get_user_cart(request,user,db)
    return {"items":cart.items,"total":cart.total_cost()}
@router.put("/cart/additem")
def add_item_cart(request:Request,product:CartItemCreate,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return add_cartitems(request,user,product,db)

@router.put("/cart/updateitem")
def update_item_cart(request:Request,product:CartItemUpdate,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return modify_cartitems(request,user,product,db)

@router.delete("/cart/deleteitem")
def delete_item_cart(request:Request,product:CartItemDelete,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return delete_cart_item(request,user,product,db)

@router.put("/cart/clearcart")
def cart_item(request:Request,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return clear_cart(request,user,db)

@router.put("/cart/checkout")
def checkout(request:Request,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    
    return complete_order(request,user,db)