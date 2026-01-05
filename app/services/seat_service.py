from app.db.models.seat import Seat
from app.services.base_service import BaseService
from app.services.event_service import EventService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.config.config import Messages

class SeatService(BaseService[Seat]):
    model = Seat

    @staticmethod
    async def get_seats_by_event(db: AsyncSession, event_id: int) -> list[Seat]:
        if not await EventService.check_event_exists(db, event_id):
            raise ValueError(Messages.EVENT_NOT_FOUND)

        result = await db.execute(select(Seat).where(Seat.event_id == event_id))
        return result.scalars().all()
    