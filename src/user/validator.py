from pydantic import BaseModel, field_validator
import re

class UserUpdateRequest(BaseModel):
    name: str

    @field_validator('name')
    @classmethod
    def validate_name(cls, v):
        if not re.match(r'^[a-zA-Z ]{3,}$', v):
            raise ValueError('Name must be at least 3 characters long and contain only letters (a-z, A-Z) and spaces')
        return v