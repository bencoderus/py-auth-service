import os
import json
from redis import Redis
from typing import Any, Optional


class RedisClient:
    """Redis client wrapper for set and get operations."""
    
    def __init__(self):
        self.client = Redis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            db=int(os.getenv("REDIS_DB", 0)),
            decode_responses=True
        )
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """
        Set a key-value pair in Redis.
        
        Args:
            key: The key to set
            value: The value to store (will be JSON serialized)
            ttl: Time to live in seconds (optional)
        
        Returns:
            True if successful
        """
        try:
            serialized_value = json.dumps(value)
            if ttl:
                self.client.setex(key, ttl, serialized_value)
            else:
                self.client.set(key, serialized_value)
            return True
        except Exception as e:
            print(f"Error setting key {key}: {e}")
            return False
    
    def get(self, key: str) -> Optional[Any]:
        """
        Get a value from Redis.
        
        Args:
            key: The key to retrieve
        
        Returns:
            The deserialized value or None if key doesn't exist
        """
        try:
            value = self.client.get(key)
            if value is None:
                return None
            return json.loads(value)
        except Exception as e:
            print(f"Error getting key {key}: {e}")
            return None


# Global Redis client instance
redis_client = RedisClient()
