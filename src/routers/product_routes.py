
from re import S
from fastapi import FastAPI,Depends,APIRouter, HTTPException,Request
from requests import Session
from database import SessionLocal,get_db
from utils.helper_functions import create_user,login_user
from schema.schema import CreateUser,CategoryBase,CategoryUpdate
from utils.helper_functions import get_current_user
from models.product_model import Category
router =APIRouter()

@router.post("/category")
def create_category(request:Request,category:CategoryBase,db:Session=Depends(get_db)):
    obj=db.query(Category).filter(Category.name==category.name).first()
    if obj:
        raise HTTPException(status_code=400,detail="Category name exists")
    new_category=Category(
        name=category.name,
        description=category.description

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


