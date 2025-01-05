from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Float, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import uuid
from .base import Base
from datetime import datetime


class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True)
    name = Column(String(255))
    bio = Column(Text, nullable=True)
    phone = Column(String(50), nullable=True)
    photo_url = Column(String(255), nullable=True)
    is_active = Column(Boolean, default=True)
    user_metadata = Column(JSONB, default={})  # Changed from 'metadata' to 'user_metadata'
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    oauth_provider = Column(String(50), nullable=True)
    oauth_id = Column(String(255), nullable=True)