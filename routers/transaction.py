from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, func,Numeric
from typing import List
import models, schemas
from database import get_db
import oauth2


router = APIRouter(
    tags=["Transactions"]
) 

# Dashboard
@router.get("/dashboard", status_code=status.HTTP_200_OK, response_model=schemas.DashboardResponse)
def dashboard(current_user:models.User=Depends(oauth2.get_current_user), db: Session = Depends(get_db)):   
    total_income = db.query(func.sum(models.Transactions.transaction_amount))\
                      .filter(models.Transactions.owner_id == current_user.id, models.Transactions.transaction_type == "income")\
                      .scalar()

    total_expense = db.query(func.sum(models.Transactions.transaction_amount))\
                       .filter(models.Transactions.owner_id == current_user.id, models.Transactions.transaction_type == "expense")\
                       .scalar()
    
    average_expense = db.query(func.round(
        func.cast(func.avg(models.Transactions.transaction_amount), Numeric),
        2)).filter( models.Transactions.owner_id == current_user.id,
    models.Transactions.transaction_type == "expense").scalar()
    
    total_transaction = db.query(func.count(models.Transactions.id))\
                       .filter(models.Transactions.owner_id == current_user.id)\
                       .scalar()
    
    current_income = total_income or 0
    current_expense = total_expense or 0
    average_expense = average_expense or 0
    total_transaction = total_transaction or 0
   
    balance = current_income - current_expense

    #recent transaction section
    recenttransaction = db.query(models.Transactions).filter(models.Transactions.owner_id == current_user.id).order_by(models.Transactions.id.desc()).limit(10).all()
    

    return {
        "total_income": current_income,
        "total_expense": current_expense,
        "balance": balance,
        "average_expense": average_expense,
        "total_transactions": total_transaction,
        "recent_transactions":recenttransaction
    }

# Add Transaction
@router.post("/add-transaction", status_code=status.HTTP_201_CREATED, response_model=schemas.TransactionCreateResponse)
def add_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    if transaction.transaction_amount <= 0:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="amount should be greater than zero")
    new_transaction = models.Transactions(owner_id=current_user.id,**transaction.model_dump())
    
    db.add(new_transaction)
    db.commit()
    db.refresh(new_transaction)
    return new_transaction



# All Transactions (Pagination + Search)
@router.get("/all-transactions", status_code=status.HTTP_200_OK, response_model=schemas.AlltransactionResponse)
def all_transaction(search: str = "", skip: int = 0, limit: int = 10, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    query = db.query(models.Transactions).filter(models.Transactions.owner_id == current_user.id).order_by(models.Transactions.id.desc())
    if search:
        query = query.filter(or_(models.Transactions.transaction_name.startswith(search), models.Transactions.transaction_description.contains(search)))
    transactions = query.offset(skip).limit(limit+1).all()
    has_next = False
    if len(transactions) > limit:
        has_next = True
        transactions = transactions[:limit]
    return {"data": transactions, "has_next": has_next}

# Delete Transaction
@router.delete("/delete-transaction/{transaction_id}", status_code=status.HTTP_200_OK)
def delete_transaction(transaction_id: int, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    transaction = db.query(models.Transactions).filter(models.Transactions.id == transaction_id,models.Transactions.owner_id==current_user.id).first()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "successfully deleted"}

# Edit Transaction
@router.put("/transactions/{transaction_id}", response_model=schemas.TransactionCreateResponse, status_code=status.HTTP_202_ACCEPTED)
def edit_transaction(transaction_id: int, updated_transaction: schemas.TransactionCreate, db: Session = Depends(get_db),current_user:models.User=Depends(oauth2.get_current_user)):
    transaction_query = db.query(models.Transactions).filter(models.Transactions.id == transaction_id,models.Transactions.owner_id==current_user.id)
    transaction = transaction_query.first()
    if transaction is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="transaction not found")
    
    transaction_query.update(updated_transaction.model_dump(), synchronize_session=False)
    db.commit()
    return transaction_query.first()
@router.get("/transactions/{transaction_id}", status_code=status.HTTP_200_OK,response_model=schemas.TransactionCreateResponse)
async def get_single_transaction(transaction_id: int, user: dict = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    transaction = db.query(models.Transactions).filter(
        models.Transactions.id == transaction_id, 
        models.Transactions.owner_id == user.id 
    ).first()

    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return transaction