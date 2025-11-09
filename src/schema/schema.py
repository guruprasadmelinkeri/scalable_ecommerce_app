from re import I
from pydantic import BaseModel
from typing import List, Optional



class CreateUser(BaseModel):
    username:str
    password:str
    email:str


## cartitem schemas
class CartItemBase(BaseModel):
    product_id:int
    quantity:int

class CartItemCreate(CartItemBase):
    pass

class CartItemRead(CartItemBase):
    id:int
    product_id:int
    price_at_addition:float
    quantity:int
    subtotal=float

    class Config:
        orm_mode = True


class CartItemUpdate(CartItemBase):
    quantity:Optional[int]=None

## cart schemas

class CartRead(BaseModel):
    id:int
    user_id:int
    items=List[CartItemRead]
    total:float

    class Config:
        orm_mode = True

## product schemas 

class CategoryBase(BaseModel):
    name:str
    description:Optional[str]=None

class CategoryRead(CategoryBase):
    id:int

    class Config:
        orm_mode=True

class ProductBase(BaseModel):
    name:str
    description:Optional[str]=None
    price:float
    stock:int
    category_id:Optional[int]=None
    image_url:Optional[str]=None


class ProductCreate(ProductBase):
    pass 

class ProductRead(ProductBase):
    id:int
    is_active:bool 
    category:Optional[CategoryRead]

    class Config:
        orm_read:True




