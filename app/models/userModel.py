from sqlalchemy import Column, DateTime, Integer, String, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), default="")
    email = Column(String(255), default="")
    password = Column(String(255), nullable=False, default=0)
    salt = Column(String(255), default="")
    profile_id = Column(Integer, ForeignKey("user_profile.id"), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile = relationship("UserProfile")
    events = relationship("Events", back_populates="user", cascade="all, delete")
    