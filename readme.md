# Credit Management API & Database Schema

## Overview

This project is a backend API for a credit management system, built using FastAPI. It allows for user creation, managing user credits, and includes a background job to automatically update credits daily. The system uses PostgreSQL as its database.

## Key Features

- **User Management**: Create new users.
- **Credit Operations**: Add, deduct, reset, and check a user's credit balance.
- **External Update**: Directly set a user's credit balance from an external source.
- **Background Job**: An automated scheduler that adds 5 credits to every user's account daily.

---

## Technologies Used

- **Backend Framework**: FastAPI
- **Database**: PostgreSQL
- **ORM**: SQLAlchemy
- **Scheduler**: APScheduler
- **Dependencies**: uvicorn, python-dotenv, psycopg2-binary, etc.

---

## Getting Started

### Prerequisites

- Python 3.8+
- `pip` (Python package installer)
- A running PostgreSQL database instance

### Installation

1. **Clone the repository:**

    ```bash
    git clone [https://github.com/abhishekKumar253/backend-intern-credits.git](https://github.com/abhishekKumar253/backend-intern-credits.git)
    cd backend-intern-credits/backend
    ```

2. **Set up the environment:**
    Create a `.env` file in the `backend` folder with your PostgreSQL database URL.

    ```env
    DATABASE_URL="postgresql://[username]:[password]@[host]:[port]/[database_name]"
    ```

3. **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

To run the FastAPI server and the background scheduler together, open two separate terminals.

1. **Start the FastAPI server:**

    ```bash
    uvicorn src.main:app --reload
    ```

2. **Run the background job (in the second terminal):**

    ```bash
    python -m src.jobs.daily_credit
    ```

---

## API Endpoints

All API endpoints are accessible at `http://127.0.0.1:8000`.

### User Management

- **Create a new user**
  - `POST /users/`
  - **Body**: `{ "email": "user@example.com", "name": "Test User" }`

### Credit Operations

- **Get a user's current credit balance**
  - `GET /api/credits/{user_id}`
- **Add credits to a user**
  - `POST /api/credits/{user_id}/add`
  - **Body**: `{ "amount": 50 }`
- **Deduct credits from a user**
  - `POST /api/credits/{user_id}/deduct`
  - **Body**: `{ "amount": 20 }`
- **Reset a user's credits to zero**
  - `PATCH /api/credits/{user_id}/reset`
- **External update of a user's credits**
  - `POST /api/credits/{user_id}/external-update`
  - **Body**: `{ "credits": 500 }`

---

## Postman Collection

The file `Credit_Management_Postman_Collection.json` is included in the root directory for convenient API testing.

## Author

- *Abhishek Kumar**
