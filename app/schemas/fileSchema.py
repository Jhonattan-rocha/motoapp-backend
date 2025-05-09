from datetime import datetime
from pydantic import BaseModel

class FileBase(BaseModel):
    filename: str
    originalname: str
    content_type: str
    file_path: str

class FileCreate(FileBase):
    id: int

class FileResponse(FileBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
    