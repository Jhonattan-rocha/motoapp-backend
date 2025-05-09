from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.schemas.carsSchema import Car
from app.schemas.userSchema import User

class EventBase(BaseModel):
    name: str
    desc: str
    date: str
    user_id: int
    car_id: int

class EventCreate(EventBase):
    id: int


class Event(EventBase):
    id: int
    cars: Optional["Car"]
    user: Optional["User"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
