from app.db.models.ticket import Ticket, TicketStatus
from app.services.base_service import BaseService
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.config.config import Messages

class TicketService(BaseService[Ticket]):
    model = Ticket

    @staticmethod
    async def list_by_payment(db: AsyncSession, payment_id: int) -> list[Ticket]:
        result = await db.execute(
            select(Ticket).where(Ticket.payment_id == payment_id)
        )
        return result.scalars().all()

    @staticmethod
    async def create_pending_ticket(db: AsyncSession, user_id: int, seat_id: int, payment_id: int) -> Ticket:
        try:
            if not await UserService.check_user_exists(db, user_id):
                raise ValueError(Messages.USER_NOT_FOUND)
            
            ticket = Ticket(
                user_id=user_id,
                seat_id=seat_id,
                payment_id=payment_id,
                status=TicketStatus.PENDING
            )
            db.add(ticket)
            await db.flush()
            await db.refresh(ticket)
            return ticket
        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_tickets_by_user(db: AsyncSession, user_id: int) -> list[Ticket]:
        if not await UserService.check_user_exists(db, user_id):
            raise ValueError(Messages.USER_NOT_FOUND)

        result = await db.execute(
            select(Ticket).where(Ticket.user_id == user_id)
        )
        return result.scalars().all()
