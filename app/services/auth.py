import requests
from fastapi import APIRouter, Depends, Request
from authlib.integrations.starlette_client import OAuth
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import users
from ..core import security as auth
from app.core.config import settings
from ..schemas import users as uS

async def register_user(db: Session, user_data: uS.UserCreate):
    if db.query(users.User).filter(users.User.email == user_data.email).first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user_data.password)
    db_user = users.User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name
    )
    db.add(db_user)
    db.commit()
    return db_user

async def create_token(db: Session, email: str, password: str):
    user = db.query(users.User).filter(users.User.email == email).first()
    if not user or not auth.verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    return auth.create_access_token(user.email)

async def login_user(db:Session, login_data):
    user = db.query(users.User).filter(users.User.email == login_data.email).first()

    # Verify user exists and password is correct
    if not user or not auth.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email},
        expires_delta=access_token_expires
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={
        "scope": "openid email profile",
        'redirect_uri': settings.GOOGLE_REDIRECT_URL # Update this to match your endpoint
    }
)

async def google_login(request: Request):
    """Initiate Google OAuth Login with proper state handling."""
    try:
        return await oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URL)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f"Failed to initiate Google login: {str(e)}"
        )

async def google_callback(request: Request, db: Session):
    """Handle Google OAuth callback"""
    try:
        # Get access token and user info
        token = await oauth.google.authorize_access_token(request)

        # Try getting user info from token
        user_info = token.get('userinfo')
        if not user_info:
            # If not in token, try parsing ID token
            user_info = await oauth.google.parse_id_token(request, token)

        if not user_info:
            raise HTTPException(status_code=400, detail="Failed to get user info from Google")

        # Check if user exists
        user = db.query(users.User).filter(users.User.email == user_info['email']).first()

        if not user:
            # Create new user
            user = users.User(
                email=user_info['email'],
                name=user_info.get('name', ''),
                photo_url=user_info.get('picture', ''),
                oauth_provider='google'
            )
            db.add(user)
            db.commit()
            db.refresh(user)

        # Generate access token
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = auth.create_access_token(
            data={"sub": user.email},
            expires_delta=access_token_expires
        )

        # Clear the session after successful authentication
        request.session.clear()

        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "email": user.email,
                "name": user.name,
                "photo_url": user.photo_url
            }
        }

    except Exception as e:
        # Clear session in case of error
        request.session.clear()
        raise HTTPException(status_code=400, detail=f"Authentication failed: {str(e)}")