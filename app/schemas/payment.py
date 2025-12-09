from pydantic import BaseModel, DateTime
from typing import Optional

class PaymentBase(BaseModel):
    user_id: int
    amount: float
    provider: str
    status: str
    created_at: DateTime
    updated_at: DateTime

class PaymentCreate(PaymentBase):
    user_id: int
    amount: float
    provider: str
    status: str
    created_at: DateTime
    updated_at: DateTime
    
class PaymentUpdate(BaseModel):
    user_id: Optional[int] = None
    amount: Optional[float] = None
    provider: Optional[str] = None
    status: Optional[str] = None
    created_at: Optional[DateTime] = None
    updated_at: Optional[DateTime] = None

class PaymentRead(PaymentBase):
    id: int

    class Config:
        orm_mode = True
