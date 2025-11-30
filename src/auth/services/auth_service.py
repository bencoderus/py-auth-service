from src.auth.services import jwt_service
from src.auth.validator import RegisterRequest, LoginRequest
from src.auth.services.password_hash import hash_password, verify_password
from src.user import repository
from fastapi import HTTPException
from os import getenv


async def authenticate_user(db, request: LoginRequest):
    user = await repository.get_user_by_email(db, request.email)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    password_matches = verify_password(request.password, user["password"])

    if not password_matches:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    jwt_secret = getenv("JWT_SECRET")
    if not jwt_secret:
        raise HTTPException(status_code=500, detail="JWT_SECRET not configured")

    token = jwt_service.create_token(str(user["id"]), jwt_secret)

    return {"user": repository.format_user_data(user), "token": token}


async def register(db, request: RegisterRequest):
    exists = await repository.get_user_by_email(db, request.email)
    if exists:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_password = hash_password(request.password)
    user_data = request.model_dump()
    user_data["password"] = hashed_password.decode("utf-8")
    created = await repository.create_user(db, user_data)

    return repository.format_user_data(created)
