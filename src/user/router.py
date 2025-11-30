from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.common.dependencies.authenticate import authenticate_request
from src.user.validator import UserUpdateRequest
from src.user import service
from src.db import get_db

user_router = APIRouter(prefix="/user")


@user_router.get("/profile")
async def get_user(
    user_id: str = Depends(authenticate_request), db: AsyncSession = Depends(get_db)
):
    response = await service.get_user_by_id(db, user_id)
    return {
        "status": True,
        "message": "User details retrieved successfully",
        "data": response,
    }


@user_router.patch("/profile")
async def update_user(
    request: UserUpdateRequest,
    db: AsyncSession = Depends(get_db),
    user_id: str = Depends(authenticate_request),
):
    response = await service.update_user(db, user_id, request.model_dump())
    return {
        "status": True,
        "message": "User details updated successfully",
        "data": response,
    }
