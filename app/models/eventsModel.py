from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime

class Events(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(255), default="")
    date = Column(String, default=str(datetime.now()))
    desc = Column(String, default="")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    cars = relationship("Cars", cascade="all, delete")
