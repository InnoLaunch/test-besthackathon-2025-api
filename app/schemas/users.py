from pydantic import BaseModel
from app.models.user import UserRole


class UserBase(BaseModel):
    username: str
    role: UserRole

    class Config:
        from_attributes = True


class User(UserBase):
    pass


class SignupUser(UserBase):
    password: str
