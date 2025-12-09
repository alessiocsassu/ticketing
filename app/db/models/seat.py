from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLAlchemyEnum, ForeignKey
from app.db.models.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

# In case of relationships in the future
# from sqlalchemy.orm import relationship

class SeatStatus(Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    SOLD = "SOLD"


class Seat(Base):
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    row = Column(String, nullable=False)
    column = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(SeatStatus), default=SeatStatus.AVAILABLE, nullable=False)
    price = Column(Float, nullable=False)
    reservated_at = Column(DateTime, nullable=True)

    event = relationship("Event", back_populates="seats")