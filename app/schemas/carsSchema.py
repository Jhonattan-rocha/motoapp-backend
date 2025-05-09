from pydantic import BaseModel
from datetime import datetime

class CarBase(BaseModel):
    name: str

class CarCreate(CarBase):
    id: int

class Car(CarBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True