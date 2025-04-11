from pydantic import BaseModel
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str

    class Config:
        from_attributes = True


class User(UserBase):
    role: UserRole


class SignupUser(UserBase):
    password: str
