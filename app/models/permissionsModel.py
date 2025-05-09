from sqlalchemy import Column, DateTime, Integer, String, Boolean, ForeignKey, func
from sqlalchemy.orm import relationship
from app.database import Base


class Permissions(Base):
    __tablename__ = 'permissions'

    id = Column(Integer, primary_key=True)
    entity_name = Column(String(255), nullable=False)
    can_view = Column(Boolean, default=False)
    can_delete = Column(Boolean, default=False)
    can_update = Column(Boolean, default=False)
    can_create = Column(Boolean, default=False)
    profile_id = Column(Integer, ForeignKey('user_profile.id'), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    profile = relationship("UserProfile", back_populates="permissions")
