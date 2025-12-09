from pydantic import BaseModel
from typing import Optional

class TicketBase(BaseModel):
    user_id: int
    seat_id: int
    payment_id: int
    status: str

class TicketCreate(TicketBase):
    user_id: int
    seat_id: int
    payment_id: int
    status: str
    
class TicketUpdate(BaseModel):
    user_id: Optional[int] = None
    seat_id: Optional[int] = None
    payment_id: Optional[int] = None
    status: Optional[str] = None

class TicketRead(TicketBase):
    id: int

    class Config:
        orm_mode = True
