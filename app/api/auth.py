from fastapi import APIRouter, Depends, Request,HTTPException, status, UploadFile, File
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from ..schemas import users  # Changed from ..schemas
from ..services import auth as auth_service  # Changed from ..services
from app.db.connection import get_db

router = APIRouter()

@router.post("/register", response_model=users.User)
async def register(user: users.UserCreate, db: Session = Depends(get_db)):
    print(user)
    return await auth_service.register_user(db, user)

@router.post("/token", response_model=users.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    return await auth_service.create_token(db, form_data.username, form_data.password)

@router.post("/login", response_model=users.Token)
async def login(login_data: users.LoginRequest, db: Session = Depends(get_db)):
    return await auth_service.login_user(db, login_data)

@router.get("/google")
async def google_login(request: Request):
    return await auth_service.google_login(request)

@router.get("/google/callback")
async def google_callback(request: Request, db: Session = Depends(get_db)):
    return await auth_service.google_callback(request, db)