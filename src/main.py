from fastapi import FastAPI,Request
from requests import session
from auth.create_tokens import SECRET_KEY
from database import Base,engine
from routers.user_routes import router as user_router
from starlette.middleware.sessions import SessionMiddleware
from dotenv import load_dotenv
import os


app=FastAPI()
app.include_router(user_router)

app.add_middleware(SessionMiddleware,
    secret_key=SECRET_KEY,
    session_cookie="session",
    same_site="lax",
    https_only=True,
    )

Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"the api is running "}