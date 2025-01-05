from pydantic import BaseModel
from typing import List, Optional

class CandleData(BaseModel):
    timestamp: int
    open: float
    high: float
    low: float
    close: float
    volume: float
    close_time: int
    quote_volume: float
    trades: int
    taker_base_volume: float
    taker_quote_volume: float