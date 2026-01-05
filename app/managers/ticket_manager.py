from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.managers.base_manager import BaseManager
from app.services.ticket_service import TicketService
from app.services.payment_service import PaymentService
from app.services.seat_service import SeatService
from app.config.redis import lock_seat, unlock_seat, check_seat_locked, get_seat_lock_owner
from app.db.models.ticket import Ticket, TicketStatus
from app.db.models.payment import PaymentStatus
from app.db.models.seat import SeatStatus
from app.config.config import Messages


class TicketManager(BaseManager[Ticket, TicketService]):
    service = TicketService

    @staticmethod
    async def reserve_seats(db: AsyncSession, user_id: int, seat_ids: list[int]) -> dict:
        locked = []

        for seat_id in seat_ids:
            lock = await lock_seat(seat_id, user_id)
            if not lock:
                for seat in locked:
                    await unlock_seat(seat)
                raise HTTPException(400, Messages.SEAT_NOT_AVAILABLE)
            locked.append(seat_id)

        for seat_id in seat_ids:
            await SeatService.set_reserved(db, seat_id)
            await TicketService.create_pending_ticket(db, user_id, seat_id)

        await db.commit()
        return {"reserved": seat_ids}
    
    @staticmethod
    async def confirm_payment(db: AsyncSession, payment_id: int):
        # Mettere i messaggi di errore in config
        payment = await PaymentService.get_by_id(db, payment_id)
        if not payment:
            raise HTTPException(404, "Payment not found")

        tickets = await TicketService.list_by_payment(db, payment_id)
        if not tickets:
            raise HTTPException(400, "No tickets associated with this payment")

        for ticket in tickets:
            owner = await get_seat_lock_owner(ticket.seat_id)
            if owner is None:
                raise HTTPException(400, "Reservation expired")
            if str(owner) != str(ticket.user_id):
                raise HTTPException(400, "Seat reserved by another user")
            
        payment.status = PaymentStatus.SUCCEEDED
        await PaymentService.update(db, payment_id, payment)

        for ticket in tickets:
            ticket.status = TicketStatus.PAID
            await TicketService.update(db, ticket.id)

            seat = await SeatService.get_by_id(db, ticket.seat_id)
            if seat:
                seat.status = SeatStatus.SOLD
            await SeatService.set_sold(db, ticket.seat_id)

            await unlock_seat(ticket.seat_id)

        await db.commit()
        return {"status": "payment_confirmed"}

    @staticmethod
    async def expire_reservations(db: AsyncSession):

        expired_seats = []

        await db.commit()
        return {"expired": expired_seats}
