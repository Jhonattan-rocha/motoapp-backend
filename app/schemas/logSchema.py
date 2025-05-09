from pydantic import BaseModel
import datetime
from typing import Optional
from app.schemas.userSchema import User

class LoggerBase(BaseModel):
    user_id: int
    entity: str
    data: str = datetime.datetime.now()
    action: str

class LoggerCreate(LoggerBase):
    id: int


class Logger(LoggerBase):
    id: int
    user: Optional[User]
    created_at: datetime.datetime
    updated_at: datetime.datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
