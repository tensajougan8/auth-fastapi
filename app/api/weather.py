from fastapi import APIRouter, Depends
from ..models import users as user
from ..services import weather as weather_service
from ..core.security import get_current_user
from ..db.connection import get_db
from ..models import users as user_model

router = APIRouter(prefix="/weather", tags=["weather"])

@router.get("")
async def get_weather(current_user: user.User = Depends(get_current_user)):
    return await weather_service.get_weather()