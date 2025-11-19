from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import complete_delivery, complete_payment, create_user,login_user,start_shipping
from schema.schema import CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate,ShippingRequest,DeliveryRequest,PaymentRequest
from utils.helper_functions import get_current_user
from models.product_model import Category, Product
router =APIRouter()

@router.put("/user/orders/pay")
def pay_order(request:Request,payload:PaymentRequest,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return complete_payment(request,user,payload,db)

@router.put("/user/orders/ship")
def ship_order(request:Request,payload:ShippingRequest,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return start_shipping(request,user,payload,db)

@router.put("/user/orders/deliverey")
def deliver_order(request:Request,payload:DeliveryRequest,db:Session=Depends(get_db)):
    user=get_current_user(db,request)
    return complete_delivery(request,user,payload,db)