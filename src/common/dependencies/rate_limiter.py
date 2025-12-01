from fastapi import Request, HTTPException
from datetime import datetime, timedelta
from src.common.redis_client import redis_client


def get_ip(request: Request):
    return (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.client.host
    )


def rate_limit(requests: int, period: int):
    """
    Rate limiter dependency that allows a specified number of requests within a time period.
    Uses Redis to store request timestamps for distributed rate limiting.
    
    Args:
        requests: Number of requests allowed
        period: Time period in seconds
    
    Returns:
        A dependency function that checks rate limits
    """
    async def rate_limiter(request: Request) -> None:
        client_ip = get_ip(request)
        now = datetime.now()
        key = f"rate_limit:{client_ip}"
        
        # Get current request history from Redis
        request_times = redis_client.get(key) or []
        
        # Clean up old requests outside the time window
        cutoff_time = (now - timedelta(seconds=period)).isoformat()
        request_times = [req_time for req_time in request_times if req_time > cutoff_time]
        
        # Check if client has exceeded rate limit
        if len(request_times) >= requests:
            raise HTTPException(
                status_code=429,
                detail=f"Rate limit exceeded. Maximum {requests} requests per {period} seconds allowed."
            )
        
        # Record this request
        request_times.append(now.isoformat())
        redis_client.set(key, request_times, ttl=period)
    
    return rate_limiter