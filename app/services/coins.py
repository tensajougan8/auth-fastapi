import requests
from datetime import timedelta
from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from ..models import users, coins
from ..core import security as auth
from ..core.config import settings
from ..schemas import users as uS
from ..schemas import crypto

async def get_all_coins():
    response = requests.get("https://api.binance.com/api/v3/ticker/24hr")
    return response.json()

async def get_coin(db: Session, current_user: users.User, symbol: str):
    url = f"https://api.binance.com/api/v3/ticker"
    query = {
        "symbol": symbol.upper()
    }
    response = requests.get(url, params=query)
    data = response.json()
    return data

async def get_coin_graph_data(db: Session, current_user: users.User, symbol: str,
                            interval: str, start_time: int, end_time: int):
    url = f"https://api.binance.com/api/v3/klines"

    params = {
        "symbol": symbol.upper(),
        "interval": interval,
        "startTime": start_time,
        "endTime": end_time
    }
    
    response = requests.get(url, params=params)
    data = response.json()

    # Transform the kline data into array of objects
    formatted_data = [
        crypto.CandleData(
            timestamp=entry[0],
            open=float(entry[1]),
            high=float(entry[2]),
            low=float(entry[3]),
            close=float(entry[4]),
            volume=float(entry[5]),
            close_time=entry[6],
            quote_volume=float(entry[7]),
            trades=int(entry[8]),
            taker_base_volume=float(entry[9]),
            taker_quote_volume=float(entry[10])
        ) for entry in data
    ]

    # Log the request to watch history
    if formatted_data:
        watch = coins.CoinWatch(
            user_id=current_user.id,
            symbol=symbol,
            last_price=formatted_data[-1].close,
            price_change=((formatted_data[-1].close - formatted_data[0].close) / formatted_data[0].close * 100)
        )
        db.add(watch)
        db.commit()

    return formatted_data