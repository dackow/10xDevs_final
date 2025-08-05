from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Request, Form
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse, RedirectResponse, Response
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud import crud
from app.schemas.schemas import Token, User, UserCreate
from app.services import auth_service
from app.config import ACCESS_TOKEN_EXPIRE_MINUTES
from ..dependencies import get_db

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    try:
        return crud.create_user(db=db, user=user)
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already registered")

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = auth_service.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/login")
async def login_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if not username or not password:
        return templates.TemplateResponse("login.html", {"request": request, "error_message": "Nazwa użytkownika i hasło są wymagane."})
    
    user = auth_service.authenticate_user(db, username, password)
    if not user:
        return templates.TemplateResponse("login.html", {"request": request, "error_message": "Nieprawidłowa nazwa użytkownika lub hasło."})
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth_service.create_access_token(
        data={"sub": user.username},
        expires_delta=access_token_expires
    )
    
    response = Response(status_code=status.HTTP_303_SEE_OTHER)
    response.headers["Location"] = "/dashboard"
    response.set_cookie(
        key="access_token", 
        value=f"Bearer {access_token}", 
        httponly=True, 
        max_age=int(access_token_expires.total_seconds()),
        samesite="Lax", # or "Strict"
        secure=False # Set to True in production with HTTPS
    )
    return response

@router.get("/register", response_class=HTMLResponse)
async def register_page(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@router.post("/register", response_class=HTMLResponse)
async def register_user(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    if not username or not password:
        return templates.TemplateResponse("register.html", {"request": request, "error_message": "Nazwa użytkownika i hasło są wymagane."})
    
    try:
        user_in = UserCreate(username=username, password=password)
        crud.create_user(db=db, user=user_in)
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    except HTTPException as e:
        return templates.TemplateResponse("register.html", {"request": request, "error_message": e.detail})
    except IntegrityError:
        return templates.TemplateResponse("register.html", {"request": request, "error_message": "Nazwa użytkownika jest już zajęta."})

@router.post("/logout")
def logout_user():
    # Logic for user logout
    pass
