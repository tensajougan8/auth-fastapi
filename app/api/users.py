from fastapi import APIRouter, Depends, File, UploadFile
from sqlalchemy.orm import Session
from ..schemas import users as user_scehma
from ..services import users as user_service
from ..core.security import get_current_user
from ..db.connection import get_db
from ..models import users as user_model

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=user_scehma.User)
async def read_users_me(current_user: user_model.User = Depends(get_current_user)):
    return current_user

@router.put("/me", response_model=user_scehma.User)
async def update_user(
    user_update: user_scehma.UserUpdate,
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await user_service.update_user(db, current_user, user_update)

@router.post("/me/photo")
async def upload_photo(
    file: UploadFile = File(...),
    current_user: user_model.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await user_service.upload_photo(db, current_user, file)