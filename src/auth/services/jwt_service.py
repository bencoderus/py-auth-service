import jwt
from datetime import datetime, timedelta, timezone

def create_token(user_id: str, secret: str, access_token_expires_minutes: int = 60, refresh_token_expires_days: int = 7) -> dict:
    """
    Create access and refresh tokens with expiration timestamps.
    
    Returns:
        dict: Contains accessToken, refreshToken, expiresAt, and refreshExpiresAt
    """
    now = datetime.now(timezone.utc)
    
    access_token_expires = now + timedelta(minutes=access_token_expires_minutes)
    access_payload = {
        "user_id": user_id,
        "type": "access",
        "exp": access_token_expires,
        "iat": now
    }
    access_token = jwt.encode(access_payload, secret, algorithm="HS256")
    refresh_token_expires = now + timedelta(days=refresh_token_expires_days)
    refresh_payload = {
        "user_id": user_id,
        "type": "refresh",
        "exp": refresh_token_expires,
        "iat": now
    }
    refresh_token = jwt.encode(refresh_payload, secret, algorithm="HS256")
    
    return {
        "accessToken": access_token,
        "refreshToken": refresh_token,
        "expiresAt": access_token_expires.isoformat(),
        "refreshExpiresAt": refresh_token_expires.isoformat()
    }


def verify_token(token: str, secret: str) -> dict:
    """Verify and decode a JWT token."""
    return jwt.decode(token, secret, algorithms=["HS256"], options={"verify_signature": True, "verify_exp": True})