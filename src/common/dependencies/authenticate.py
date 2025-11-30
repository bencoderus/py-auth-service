from fastapi import Header, HTTPException
from src.auth.services.jwt_service import verify_token
from os import getenv
from typing import Optional

def authenticate_request(authorization: Optional[str] = Header(None)):
    """
    Authenticate a request by validating the JWT token in the Authorization header.
    Expects format: "Bearer <token>"
    Returns the user ID if valid, raises an exception if not.
    """
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header missing")
    
    # Extract token from "Bearer <token>" format
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=401, detail="Invalid authorization header format. Expected: Bearer <token>")
    
    token = parts[1]
    
    jwt_secret = getenv("JWT_SECRET")
    if not jwt_secret:
        raise HTTPException(status_code=500, detail="JWT_SECRET not configured")
    
    try:
        payload = verify_token(token, jwt_secret)

        return payload['user_id']
    except Exception as e:
        print(f"Token verification failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid or expired token")