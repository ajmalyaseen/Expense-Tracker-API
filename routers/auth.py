from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
import models, schemas, utils
from database import get_db  
import   oauth2        
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
router = APIRouter(
    tags=["Authentication"] 
)

@router.post("/user-register", status_code=status.HTTP_201_CREATED, response_model=schemas.UserCreateResponse)
def user_register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user=db.query(models.User).filter(models.User.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="user alredy exist with this mail")
    
    user.password = utils.hashing_password(user.password)
    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/user-login", status_code=status.HTTP_200_OK)
def user_login(logincred:OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == logincred.username).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    
    password = utils.verify(logincred.password, user.password)
    if not password:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="invalid credentials")
    access_token = oauth2.create_access_token(data={"user_id": user.id})

    return {"access_token": access_token, "token_type": "bearer","user_name":user.user_name}
    