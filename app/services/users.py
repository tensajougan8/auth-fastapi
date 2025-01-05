import requests
from datetime import timedelta
from fastapi import HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from ..models import users
from ..core import security as auth
from ..core.config import settings
from ..schemas import users as uS

async def update_user(db: Session, current_user: users.User, user_update: uS.UserUpdate):
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(current_user, field, value)
    db.commit()
    db.refresh(current_user)
    return current_user

async def upload_photo(db: Session, current_user: users.User, file: UploadFile):
    current_user.photo_url = file.filename
    db.commit()
    return {"filename": file.filename}