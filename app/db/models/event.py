from sqlalchemy import Column, Integer, String, DateTime
from app.db.models.base import Base

# In case of relationships in the future
# from sqlalchemy.orm import relationship

class Event(Base):
    __tablename__ = "events"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    date = Column(DateTime, nullable=False)