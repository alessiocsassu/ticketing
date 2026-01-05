from app.db.models.payment import Payment, PaymentStatus
from app.services.base_service import BaseService
from app.services.user_service import UserService
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from app.config.config import Messages
from datetime import DateTime

class PaymentService(BaseService[Payment]):
    model = Payment

    @staticmethod
    async def create_pending_payment(db: AsyncSession, user_id: int, amount: float, provider: str) -> Payment:
        try:
            if not await UserService.check_user_exists(db, user_id):
                raise ValueError(Messages.USER_NOT_FOUND)

            payment = Payment(
                user_id=user_id,
                amount=amount,
                provider=provider,
                status=PaymentStatus.PENDING,
                created_at=DateTime.now(),
                updated_at=DateTime.now()
            )
            db.add(payment)
            await db.flush()
            await db.refresh(payment)
            return payment
        except SQLAlchemyError:
            await db.rollback()
            raise

    @staticmethod
    async def get_payments_by_user(db: AsyncSession, user_id: int) -> list[Payment]:
        if not await UserService.check_user_exists(db, user_id):
            raise ValueError(Messages.USER_NOT_FOUND)

        result = await db.execute(
            select(Payment).where(Payment.user_id == user_id)
        )
        return result.scalars().all()