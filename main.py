from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine
import models
from routers import auth,transaction # 👈 New Routers Imported

# Create Tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = [
    "http://localhost:3000", 
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)

# 👇 Connecting the routers
app.include_router(auth.router)
app.include_router(transaction.router)

@app.get("/")
def home():
    return {"message": "Expense Tracker API is running like a horse! 🐎"}




    

 






















