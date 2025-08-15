from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from contextlib import asynccontextmanager  
from pydantic import BaseModel

from src.database.connection import engine, Base, SessionLocal
from src.models.users import User
from src.models.credits import Credit
from src.routes import credits
from src.jobs import daily_credit

class UserCreate(BaseModel):
    email: str
    name: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    print("Database tables created!")
    yield
    print("Application shutting down...")

app = FastAPI(lifespan=lifespan)

# DB dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app.include_router(credits.router)

@app.get("/")
def read_root():
    return {"message": "LawVriksh Credit Management API is running."}

@app.post("/users/")
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(email=user.email, name=user.name)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    new_credit_entry = Credit(user_id=new_user.user_id, credits=0)
    db.add(new_credit_entry)
    db.commit()

    return {"message": "User and credit entry created successfully!"}

