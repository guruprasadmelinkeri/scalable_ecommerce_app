from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import create_user,login_user
from schema.schema import CreateUser,CategoryBase,CategoryUpdate,ProductCreate,ProductUpdate
from utils.helper_functions import get_current_user
from models.product_model import Category, Product
router =APIRouter()

@router.post("/category")
def create_category(request:Request,category:CategoryBase,db:Session=Depends(get_db)):
    obj=db.query(Category).filter(Category.name==category.name).first()
    if obj:
        raise HTTPException(status_code=400,detail="Category name exists")
    new_category=Category(
        name=category.name,
        description=category.description,

    )

    db.add(new_category)
    db.commit()

    return category

@router.get("/category")
def get_all_category(request:Request,db:Session=Depends(get_db)):
    new_category=db.query(Category).all()
    return new_category
@router.get("/category/{id}")
def get_category_by_id(request:Request,id:int,db:Session=Depends(get_db)):
    ls=db.query(Category).filter(Category.id==id).first()
    if(not ls):
        raise HTTPException(status_code=400,detail="Category not found")
    return ls
@router.put("/category/{id}")
def update_category(request:Request,update:CategoryUpdate,id:int,db:Session=Depends(get_db)):
    category=db.query(Category).filter(Category.id==id).first()

    if not category:
        raise HTTPException(status_code=400,detail="Category not found")
    if not update.description:
        raise HTTPException(status_code=400,detail="please enter description ")
    
    category.description=update.description
    db.add(category)
    db.commit()
    return { category.id, category.description}

@router.delete("/category/{id}")
def delete_category(request:Request,id:int,db:Session=Depends(get_db)):
    category=db.query(Category).filter(Category.id==id).first()
    if not category:
        raise HTTPException(status_code=404,detail="user not found")
    db.delete(category)
    db.commit()
    return category

## product routers 
@router.put("/product")
def create_product(request:Request,product:ProductCreate,db:Session=Depends(get_db)):
    check=db.query(Product).filter(Product.name==product.name).first()
    if check:
        raise HTTPException(status_code=404,detail="name aldready exists")
    new_product=Product(
        name=product.name,
        category_id=product.category_id,
        description=product.description,
        stock=product.stock,
        price=product.price,
        image_url=product.image_url
    )
    db.add(new_product)
    db.commit()
    return product

@router.get("/product")
def get_all_products(request:Request,db:Session=Depends(get_db)):
    products=db.query(Product).all()
    return products
                     
@router.get("/product/{id}")
def get_product_by_id(request:Request,id:int,db:Session=Depends(get_db)):
    ls=db.query(Product).filter(Product.id==id).first()
    if(not ls):
        raise HTTPException(status_code=400,detail="product not found")
    return ls

@router.put("/product/{id}")
def update_product(request:Request,update:ProductUpdate,id:int,db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==id).first()

    if not product:
        raise HTTPException(status_code=400,detail="product not found")

    
    if update.stock:
        product.stock=update.stock
    if update.price:
        product.price=update.price


    db.add(product)
    db.commit()
    return { "name":product.name}

@router.delete("/product/{id}")
def delete_product(request:Request,id:int,db:Session=Depends(get_db)):
    product=db.query(Product).filter(Product.id==id).first()
    if not product:
        raise HTTPException(status_code=404,detail="Product Not Found")
    db.delete(product)
    db.commit()
    return product
