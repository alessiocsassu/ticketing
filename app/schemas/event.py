from pydantic import BaseModel, DateTime
from typing import Optional

class EventBase(BaseModel):
    name: str
    date: DateTime

class EventCreate(EventBase):
    name: str
    date: DateTime
    
class EventUpdate(BaseModel):
    name: Optional[str] = None
    date: Optional[DateTime] = None

class EventRead(EventBase):
    id: int

    class Config:
        orm_mode = True
