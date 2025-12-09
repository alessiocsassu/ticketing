from sqlalchemy import Column, Integer, String, DateTime, Float, Enum as SQLAlchemyEnum, ForeignKey
from app.db.models.base import Base
from sqlalchemy.orm import relationship
from enum import Enum

# In case of relationships in the future
# from sqlalchemy.orm import relationship

class PaymentStatus(Enum):
    PENDING = "PENDING"
    SUCCEEDED = "SUCCEEDED"
    FAILED = "FAILED"

class PaymentProvider(Enum):
    STRIPE = "STRIPE"
    PAYPAL = "PAYPAL"
    SQUARE = "SQUARE"

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Float, nullable=False)
    provider = Column(SQLAlchemyEnum(PaymentProvider), nullable=False)
    status = Column(SQLAlchemyEnum(PaymentStatus), default=PaymentStatus.PENDING, nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    user = relationship("User", back_populates="payments")