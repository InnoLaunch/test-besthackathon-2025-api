from sqlalchemy import Column
from sqlalchemy import (
    Integer,
    String,
    Enum as SAEnum
)
from uuid import uuid4
from enum import Enum

from core.database.base import Base


class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"


class DisabilityType(str, Enum):
    WHEELCHAIR = "wheelchair"
    HEARING = "hearing"
    VISION = "vision"
    COGNITIVE = "cognitive"
    NONE = "none"


class User(Base):
    __tablename__ = 'users'
    __keyfield__ = "user_id"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(SAEnum(UserRole, name="user_role"), nullable=False, default=UserRole.USER)
    disability_type = Column(SAEnum(DisabilityType), nullable=False, default=DisabilityType.NONE)
