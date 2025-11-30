from src.user import repository
from sqlalchemy.ext.asyncio import AsyncSession

async def get_user_by_id(db: AsyncSession, user_id: str):
    user = await repository.get_user_by_id(db, user_id)
    if user:
        return repository.format_user_data(user)
    return None

async def update_user(db: AsyncSession, user_id: str, update_request: dict):
    return await repository.update_user(db, user_id, update_request)