from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
#from app.schemas import User, UserCreate # Direct import
from app.schemas.schemas import User, UserCreate
from ..dependencies import get_db

router = APIRouter()

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")

@router.post("/register")
def register_user():
    # Logic for user registration
    pass

@router.post("/login")
def login_user():
    # Logic for user login
    pass

@router.post("/logout")
def logout_user():
    # Logic for user logout
    pass