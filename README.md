# 💰 Expense Tracker API

A secure, multi-user personal finance tracking REST API 
built with FastAPI and PostgreSQL.

## Problem It Solves
Most people track expenses in messy spreadsheets with no 
security or real-time summary. This API solves that — 
each user gets a secure, isolated account with instant 
financial insights.

## Features
- JWT-based authentication (register, login, protected routes)
- Add, edit, delete, and view transactions
- Dashboard with real-time income, expense, balance, 
  and average expense calculations
- Paginated transaction history with search
- Per-user data isolation — users can only access 
  their own transactions

## Tech Stack
- **Backend:** FastAPI, Python
- **Database:** PostgreSQL, SQLAlchemy ORM
- **Auth:** JWT (python-jose), bcrypt password hashing
- **Validation:** Pydantic v2

## API Endpoints

### Auth
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /user-register | Create new account |
| POST | /user-login | Login and get JWT token |

### Transactions
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | /dashboard | Financial summary |
| POST | /add-transaction | Add new transaction |
| GET | /all-transactions | Paginated list + search |
| GET | /transactions/{id} | Single transaction |
| PUT | /transactions/{id} | Edit transaction |
| DELETE | /delete-transaction/{id} | Delete transaction |

## Setup

1. Clone the repo
   git clone https://github.com/ajmalyaseen/expense-tracker-api

2. Install dependencies
   pip install -r requirements.txt

3. Set environment variables
   DATABASE_USERNAME=your_db_user
   DATABASE_PASSWORD=your_db_password
   DATABASE_HOSTNAME=localhost
   DATABASE_PORT=5432
   DATABASE_NAME=expense_tracker
   SECRET_KEY=your_secret_key
   ALGORITHM=HS256

4. Run the server
   uvicorn main:app --reload

5. Open API docs
   http://localhost:8000/docs