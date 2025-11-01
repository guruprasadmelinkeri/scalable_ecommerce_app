
from passlib.context import CryptContext

pwd_context=CryptContext(schemes=["bcrypt"],deprecated="auto")

def hash(password:str):
    hashed_pw=pwd_context.hash(password)
    return hashed_pw

def verify(pw:str,hashed_pw:str):
    return pwd_context.verify(pw,hashed_pw)