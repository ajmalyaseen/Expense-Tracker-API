from sqlalchemy import Column,Integer,String,Float
from database import Base
from datetime import datetime
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey
class Transactions(Base):
    __tablename__="transactions"
    id= Column(Integer,primary_key=True,index=True)
    transaction_name=Column(String)
    transaction_type=Column(String)
    transaction_description=Column(String)
    transaction_amount=Column(Float)
    transaction_date=Column(String)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User", back_populates="transactions")

class User(Base):
    __tablename__ = "users"  

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    user_name = Column(String, nullable=True) 
    
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    transactions = relationship("Transactions", back_populates="owner")

    