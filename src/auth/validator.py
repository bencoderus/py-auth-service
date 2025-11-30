from pydantic import BaseModel, EmailStr, field_validator
import re


def validate_strong_password(password: str) -> str:
    """
    Validates that a password is strong:
    - Min 8 chars
    - At least one uppercase
    - At least one lowercase
    - At least one digit
    - At least one special character
    """
    pattern = re.compile(
        r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$'
    )

    if not pattern.match(password):
        raise ValueError(
            'Password must be at least 8 characters long, include an uppercase letter, '
            'a lowercase letter, a number, and a special character.'
        )
    return password


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def strong_password(cls, v):
        return validate_strong_password(v)


class RegisterRequest(BaseModel):
    email: EmailStr
    password: str
    name: str

    @field_validator('password')
    @classmethod
    def strong_password(cls, v):
        return validate_strong_password(v)

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z ]{3,}$', v):
            raise ValueError('Name must be at least 3 characters long and contain only letters (a-z, A-Z) and spaces')
        return v
