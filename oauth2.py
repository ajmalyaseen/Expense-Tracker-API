from jose import JWTError, jwt
from fastapi import Depends,HTTPException,status
from sqlalchemy.orm import session
from datetime import datetime, timedelta
from schemas import TokenData
from fastapi.security import OAuth2PasswordBearer 
import models
import database
import config 

SECRET_KEY =  config.settings.secret_key
ALGORITHM = config.settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = 10
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="user-login")
def create_access_token(data: dict):
    
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(token:str,credentials_exceptions):
    try:
        pyload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id:str=pyload.get("user_id")
        if id is None:
            raise credentials_exceptions
    except JWTError:
        raise credentials_exceptions
    token_data=TokenData(id=id)
    return token_data

def get_current_user(token:str=Depends(oauth2_scheme),db:session=Depends(database.get_db)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_access_token(token,exception) 
    
    user = db.query(models.User).filter(models.User.id == token_data.id).first()
    return user