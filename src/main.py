from fastapi import FastAPI,Request
from database import Base,engine
from routers.user_routes import router as user_router
app=FastAPI()
app.include_router(user_router)
Base.metadata.create_all(bind=engine)
@app.get("/")
def root():
    return {"the api is running "}