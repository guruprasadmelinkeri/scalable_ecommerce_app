from re import I
from pydantic import BaseModel
from typing import List, Optional



class CreateUser(BaseModel):
    username:str
    password:str
    email:str

## product schemas 

class CategoryBase(BaseModel):
    name:str
    description:Optional[str]=None

class CategoryRead(CategoryBase):
    id:int

    class Config:
        orm_mode=True


        
class CategoryUpdate(CategoryBase):
    description:Optional[str]=None

class ProductBase(BaseModel):
    name:str
    description:Optional[str]=None
    price:float
    stock:int
    category_id:Optional[int]=None
    image_url:Optional[str]=None


class ProductCreate(ProductBase):
    pass 
class ProductUpdate(BaseModel):
    stock:Optional[int]=None
    price:Optional[int]=None
     

class ProductRead(ProductBase):
    id:int
    
    category:Optional[CategoryRead]

    class Config:
        orm_mode:True






## cartitem schemas
class CartItemBase(BaseModel):
    product_id:int
    quantity:int

class CartItemCreate(CartItemBase):
    pass
class CartItemDelete(BaseModel):
    product_id:int

class CartItemRead(CartItemBase):
    id:int
    product:ProductRead
    product_id:int
    price_at_addition:float
    quantity:int
    subtotal:float

    class Config:
        orm_mode = True


class CartItemUpdate(CartItemBase):
    quantity:Optional[int]=None

## cart schemas

class CartRead(BaseModel):
    id:int
    user_id:int
    items:List[CartItemRead]
    total:float

    class Config:
        orm_mode = True


##payment shipping and delivery schema 

class PaymentRequest(BaseModel):
    order_id:int
    user_id:int
    payment_method:Optional[str]=None

class ShippingRequest(BaseModel):
    order_id:int
    user_id:int
    shipping_method:Optional[str]="Standard"

class DeliveryRequest(BaseModel):
    order_id:int
    user_id:int
    delivery_method:Optional[str]=None




