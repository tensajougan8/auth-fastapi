from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from ..models import users as models
from ..schemas import crypto
from app.db.connection import get_db
from ..services import coins as crypto_service
from ..core.security import get_current_user


router = APIRouter(prefix="/crypto", tags=["crypto"])

@router.get("/coins")
async def get_coins(current_user: models.User = Depends(get_current_user)):
    return await crypto_service.get_all_coins()

@router.get("/coin/{symbol}")
async def get_coin(
    symbol: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    return await crypto_service.get_coin(db, current_user, symbol)

@router.get("/coin/{symbol}/graph", response_model=List[crypto.CandleData])
async def get_coin_data(
    symbol: str,
    interval: str = Query(..., description="Kline/Candlestick chart intervals"),
    start_time: Optional[int] = Query(None),
    end_time: Optional[int] = Query(None),
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    interval = interval or "1M"

    # Optionally, you could validate the interval if it must match specific values
    valid_intervals = ["1m", "3m", "5m", "15m", "30m", "1h", "2h", "4h", "6h", "8h", "12h", "1d", "3d", "1w", "1M"]
    if interval not in valid_intervals:
        raise HTTPException(status_code=400, detail="Invalid interval specified.")

    return await crypto_service.get_coin_graph_data(
        db, current_user, symbol, interval, start_time, end_time
    )