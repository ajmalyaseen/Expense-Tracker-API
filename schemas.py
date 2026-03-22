from pydantic import BaseModel,EmailStr
from typing import Literal,Optional
from datetime import datetime


#transaction schemas
class TransactionCreate(BaseModel):
    transaction_name: str           
    transaction_type: Literal['income','expense']
    transaction_description:Optional[str]=None
    transaction_amount:float
    transaction_date:str 

class TransactionCreateResponse(TransactionCreate):
    id: int
    class Config:
        from_attributes = True

class AlltransactionResponse(BaseModel):
    data:list[TransactionCreateResponse]
    has_next:bool
    class Config:
        from_attribute= True

#dashboard schemas        
class DashboardResponse(BaseModel):
    total_income: float
    total_expense: float
    balance:float
    average_expense: float
    total_transactions: int
    recent_transactions:list[TransactionCreateResponse]

#user register schemas
class UserBase(BaseModel):
    email:EmailStr
    user_name: Optional[str] = None 
    
class UserCreate(UserBase):
    password:str

class UserCreateResponse(UserBase):
    id:int
    created_at:datetime

    class Config:
        from_attributes=True

#user login schemas
class UserLogin(BaseModel):
    email:EmailStr
    password:str

# Token Response (യൂസർക്ക് തിരിച്ചു കൊടുക്കുന്നത്)
class Token(BaseModel):
    access_token: str
    token_type: str
    user_name:str

# Token Data (ടോക്കണിന്റെ ഉള്ളിൽ ഒളിപ്പിച്ചു വെക്കുന്ന ഡാറ്റ)
class TokenData(BaseModel):
    id: Optional[int] = None