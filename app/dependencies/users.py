from fastapi import Depends
from fastapi import Cookie
from fastapi.security import OAuth2PasswordBearer
from fastapi.security import HTTPBearer

from app.models.user import (
    User,
    UserRole
)
from app.repositories.users import UsersRepo
from core.security.jwthandler import (
    JWTHandler,
    TokenType
)
from core.exceptions.base import UnauthorizedException, ForbiddenException
from core.database.session import Session


oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/v1/auth/token",
    auto_error=False
)


async def get_current_user(
        token: str = Depends(oauth2_scheme)
) -> User:
    payload = JWTHandler.decode(token)
    token_type = payload.get("typ")
    if token_type != TokenType.ACCESS:
        raise UnauthorizedException("Invalid token type")
    user_id: str = payload.get("sub")
    if user_id is None or not user_id.isnumeric():
        raise UnauthorizedException("Invalid token")
    user_id = int(user_id)
    async with Session() as session:
        repo = UsersRepo(session)
        user = await repo.get(user_id=user_id)
        if not user:
            raise UnauthorizedException("Invalid token")
    return user


async def get_admin(
        user: User = Depends(get_current_user)
) -> User:
    if user.role != UserRole.ADMIN:
        raise ForbiddenException("Not enough privileges")
    return user


async def get_user_by_refresh(
        refresh_token: str = Cookie(
            None, description="HttpOnly cookie refresh token. Set empty if using SwaggerUI"
        )
) -> User:
    payload = JWTHandler.decode(refresh_token)
    token_type = payload.get("typ")
    if token_type != TokenType.REFRESH:
        raise UnauthorizedException("Invalid token type")
    user_id: str = payload.get("sub")
    if user_id is None or not user_id.isnumeric():
        raise UnauthorizedException("Invalid token")
    user_id = int(user_id)
    async with Session() as session:
        repo = UsersRepo(session)
        user = await repo.get(user_id=user_id)
        if not user:
            raise UnauthorizedException("Invalid token")
    return user