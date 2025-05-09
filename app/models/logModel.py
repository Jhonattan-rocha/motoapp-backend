from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from app.database import Base
from sqlalchemy.orm import relationship


class Logger(Base):
    __tablename__ = "logger"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    action = Column(String, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    entity = Column(String, nullable=False)
    data = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    user = relationship("User", foreign_keys="Logger.user_id", lazy="joined")