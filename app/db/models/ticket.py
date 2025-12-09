from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLAlchemyEnum, ForeignKey
from app.db.models.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

# In case of relationships in the future
# from sqlalchemy.orm import relationship

class TicketStatus(Enum):
    PENDING = "PENDING"
    PAID = "PAID"
    CANCELLED = "CANCELLED"

class Ticket(Base):
    __tablename__ = "tickets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat_id = Column(Integer, ForeignKey("seats.id"), nullable=False)
    payment_id = Column(Integer, ForeignKey("payments.id"), nullable=True)
    status = Column(SQLAlchemyEnum(TicketStatus), default=TicketStatus.PENDING, nullable=False)

    user = relationship("User", back_populates="tickets")
    seat = relationship("Seat", back_populates="tickets")
    payment = relationship("Payment", back_populates="tickets")