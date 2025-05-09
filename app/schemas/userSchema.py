from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from app.schemas.userProfileSchema import UserProfile

class UserBase(BaseModel):
    name: str
    email: str
    password: Optional[str] = ""
    salt: Optional[str] = ""
    profile_id: Optional[int] = None


class UserCreate(UserBase):
    id: int


class User(UserBase):
    id: int
    password: Optional[str] = Field(exclude=True)
    salt: Optional[str] = Field(exclude=True)
    profile: Optional["UserProfile"]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
