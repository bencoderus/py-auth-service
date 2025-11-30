from bcrypt import hashpw, checkpw, gensalt

def hash_password(password: str) -> bytes:
    salt = gensalt()
    return hashpw(password.encode(), salt)


def verify_password(password: str, hashed: str) -> bool:
    """Verify a password against a hashed password stored as string."""
    return checkpw(password.encode(), hashed.encode())
