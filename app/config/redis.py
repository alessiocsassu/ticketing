from redis.asyncio import Redis
from app.config.config import settings

redis_client = Redis(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    decode_responses=True
)

async def lock_seat(seat_id: int, user_id: int, ttl: int = 600) -> bool:
    return await redis_client.set(f"seat:{seat_id}:lock", user_id, nx=True, ex=ttl)

async def check_seat_locked(seat_id: int) -> bool:
    return await redis_client.exists(f"seat:{seat_id}:lock") == 1

async def unlock_seat(seat_id: int) -> None:
    await redis_client.delete(f"seat:{seat_id}:lock")

async def get_seat_lock_owner(seat_id: int) -> str | None:
    return await redis_client.get(f"seat:{seat_id}:lock")
