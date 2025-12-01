from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.validator import LoginRequest, RegisterRequest
from src.auth.services import auth_service
from src.common.dependencies.rate_limiter import rate_limit
from src.db import get_db

auth_router = APIRouter(prefix="/auth")

@auth_router.post("/login", status_code=200)
async def login(
    request: LoginRequest,
    _: None = Depends(rate_limit(requests=5, period=60)),
    db: AsyncSession = Depends(get_db)
):
    response = await auth_service.authenticate_user(db, request)

    return {"status": True, "message": "Login successful", "data": response}

@auth_router.post("/register", status_code=201)
async def register(
    request: RegisterRequest,
    _: None = Depends(rate_limit(requests=5, period=60)),
    db: AsyncSession = Depends(get_db)
):
    response = await auth_service.register(db, request)
    
    return {"status": True, "message": "User created successfully", "data": response}

