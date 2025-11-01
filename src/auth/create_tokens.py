import os 
from dotenv import load_dotenv

from fastapi import HTTPException
from jose import jwt
from typing import Optional

from datetime import datetime,timedelta


ALGORITHM="HS256"
load_dotenv()

SECRET_KEY=os.getenv("SECRET_KEY")

if not SECRET_KEY:
    raise HTTPException(status_code=404,detail="SECRET_KEY NOT FOUND")

def create_access_token(data:dict,expire_time:Optional[timedelta]=None):
    to_encode=data.copy()
    expires=datetime.utcnow()+(expire_time if expire_time else timedelta(minutes=60))
    to_encode.update({"exp":expires})
    encoded=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

def create_refresh_token(data:dict,expire_time:Optional[timedelta]=None):
    to_encode=data.copy()
    expires=datetime.utcnow()+(expire_time if expire_time else timedelta(days=7))
    to_encode.update({"exp":expires})
    encoded=jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded

