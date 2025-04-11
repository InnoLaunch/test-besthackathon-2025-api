from pydantic import BaseModel
from app.models.user import UserRole, DisabilityType


class UserBase(BaseModel):
    username: str
    disability_type: DisabilityType

    class Config:
        from_attributes = True


class User(UserBase):
    role: UserRole


class SignupUser(UserBase):
    password: str
