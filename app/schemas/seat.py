from pydantic import BaseModel, DateTime
from typing import Optional

class SeatBase(BaseModel):
    event_id: int
    row: str
    column: str
    status: str
    price: float
    reservated_at: DateTime

class SeatCreate(SeatBase):
    event_id: int
    row: str
    column: str
    status: str
    price: float
    reservated_at: DateTime

    
class SeatUpdate(BaseModel):
    event_id: Optional[int] = None
    row: Optional[str] = None
    column: Optional[str] = None
    status: Optional[str] = None
    price: Optional[float] = None
    reservated_at: Optional[DateTime] = None


class SeatRead(SeatBase):
    id: int

    class Config:
        orm_mode = True
