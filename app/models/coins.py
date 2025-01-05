from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSONB, UUID
from .base import Base
from datetime import datetime


class CoinWatch(Base):
    __tablename__ = "coin_watches"

    id = Column(Integer, primary_key=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    symbol = Column(String(50))
    last_price = Column(Float)
    price_change = Column(Float)
    timestamp = Column(Float)

    # Add relationship to User
    user = relationship("User", backref="coin_watches")