from app.db.models.event import Event
from app.services.base_service import BaseService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import DateTime

class EventService(BaseService[Event]):
    model = Event

    @staticmethod
    async def get_events_by_date(db: AsyncSession, date: DateTime) -> list[Event]:
        result = await db.execute(
            select(Event).where(Event.date == date)
        )
        return result.scalars().all()
    
    @staticmethod
    async def get_todays_events(db: AsyncSession, self) -> list[Event]:
        today = DateTime.now().date()
        return await self.get_events_by_date(db, today)
    
    @staticmethod
    async def check_event_exists(db: AsyncSession, event_id: int) -> bool:
        result = await db.execute(select(Event).where(Event.id == event_id))
        return result.scalar_one_or_none() is not None
