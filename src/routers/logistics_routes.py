from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from auth.rbac import require_role
from database import SessionLocal,get_db
from utils.helper_functions import complete_delivery, complete_payment, create_user,login_user,start_shipping
from schema.schema import CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate,ShippingRequest,DeliveryRequest,PaymentRequest
from utils.helper_functions import get_current_user
from models.product_model import Category, Product
router =APIRouter()

@router.put("/user/orders/pay")
def pay_order(request:Request,payload:PaymentRequest,db:Session=Depends(get_db)):
    """this route will validate user payment"""
    user=get_current_user(db,request)
    require_role(user,"admin")
    return complete_payment(request,payload,db)

@router.put("/user/orders/ship")
def ship_order(request:Request,payload:ShippingRequest,db:Session=Depends(get_db)):
    """this route will be used to ship order on request"""
    user=get_current_user(db,request)
    require_role(user,"admin")
    return start_shipping(request,payload,db)

@router.put("/user/orders/delivery")
def deliver_order(request:Request,payload:DeliveryRequest,db:Session=Depends(get_db)):
    """this route will be used to mark order as completed """

    user=get_current_user(db,request)
    require_role(user,"admin")
    return complete_delivery(request,payload,db)