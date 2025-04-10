from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import (
    Dict,
    Tuple
)
from typing import Any

from core.controller.base import BaseController
from core.exceptions.base import UnauthorizedException
from core.database.session import get_session
from app.repositories.users import UsersRepo
from app.models.user import User
from core.exceptions.base import ConflictException
from core.security.password import PasswordHandler
from core.security.jwthandler import (JWTHandler, TokenType)


class AuthCtrl(BaseController):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self.repo = UsersRepo(session)

    async def signup(
            self,
            username: str,
            password: str
    ) -> User:
        user = await self.repo.get_by(
            "username",
            username,
            unique=True
        )
        if user:
            raise ConflictException("User already exists")
        password_hash = PasswordHandler.hash(password)
        user = await self.repo.create(
            attributes={
                "username": username,
                "password_hash": password_hash
            }
        )
        await self.session.commit()
        return user

    async def token(
            self,
            username: str,
            password: str
    ) -> Tuple[Dict[str, Any], str]:
        user: User = await self.repo.get_by(
            "username",
            username,
            unique=True
        )
        if not user:
            raise UnauthorizedException("Wrong credentials")
        if not PasswordHandler.verify(user.password_hash, password):
            raise UnauthorizedException("Wrong credentials")
        refresh_token = JWTHandler.encode(sub=str(user.user_id), typ=TokenType.REFRESH)
        access_token = JWTHandler.encode(sub=str(user.user_id), typ=TokenType.ACCESS)
        return {"access_token": access_token, "token_type": "bearer"}, refresh_token

    async def refresh(
            self,
            user_id: UUID
    ) -> Dict[str, Any]:
        user: User = await self.repo.get_by(
            "user_id",
            user_id,
            unique=True
        )
        if not user:
            raise UnauthorizedException("Wrong credentials")
        access_token = JWTHandler.encode(sub=str(user.user_id), typ=TokenType.ACCESS)
        return {"access_token": access_token, "token_type": "bearer"}

