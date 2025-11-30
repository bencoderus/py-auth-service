import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text

async def get_user_by_email(db: AsyncSession, email: str):
    """
    Get user by email address.
    """
    result = await db.execute(text("SELECT * FROM users WHERE email = :email"), {"email": email})
    row = result.fetchone()
    return dict(row._mapping) if row else None

def format_user_data(user_data: dict) -> dict:
    """Format user data for response - remove password and add any necessary fields."""
    formatted = user_data.copy()
    formatted.pop('password', None)
    return formatted

async def get_user_by_id(db: AsyncSession, user_id: str):
    """
    Get user by ID.
    """
    result = await db.execute(text("SELECT * FROM users WHERE id = :id"), {"id": user_id})
    row = result.fetchone()
    return dict(row._mapping) if row else None

async def create_user(db: AsyncSession, request: dict):
    """
    Create a new user.
    """
    print(f"Creating user with data: {request}")
    user_id = str(uuid.uuid4())
    await db.execute(
        text("INSERT INTO users (id, name, email, password) VALUES (:id, :name, :email, :password)"),
        {"id": user_id, "name": request.get('name', ''), "email": request.get('email'), "password": request.get('password')}
    )
    await db.commit()

    return await get_user_by_id(db, user_id)

async def update_user(db: AsyncSession, user_id: str, update_data: dict):
    """
    Update user information.
    """
    update_fields = []
    params = {"id": user_id}
    
    for key, value in update_data.items():
        if key in ['name']: 
            update_fields.append(f"{key} = :{key}")
            params[key] = value
    
    if not update_fields:
        return await get_user_by_id(db, user_id)
    
    query = f"UPDATE users SET {', '.join(update_fields)}, updated_at = NOW() WHERE id = :id"
    await db.execute(text(query), params)
    await db.commit()
    
    return await get_user_by_id(db, user_id)
