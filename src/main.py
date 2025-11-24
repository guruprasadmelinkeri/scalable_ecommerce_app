from fastapi import FastAPI,Request
from requests import session
from auth.create_tokens import SECRET_KEY
from auth.rbac import create_admin
from database import Base,engine
from routers.user_routes import router as user_router
from routers.product_routes import router as product_router
from routers.cart_routes import router as cart_router
from routers.logistics_routes import router as logistics_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os
from scheduler.scheduler import scheduler
from scheduler.jobs import set_to_ship
from database import SessionLocal

app=FastAPI()
app.include_router(user_router)
app.include_router(product_router)
app.include_router(cart_router)
app.include_router(logistics_router)

app.add_middleware(SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session",
    same_site="lax",
    https_only=True,
    )

@app.on_event("startup")
async def start_scheduler():
    scheduler.add_job(set_to_ship, "interval", minutes=60)
    scheduler.start()

Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"the api is running "}



## execute only onnce for each admin 
##create_admin(username="username",email="email",password="password")