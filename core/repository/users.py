from sqlalchemy.ext.asyncio import AsyncSession

from core.repository.base import BaseRepository
from app.models.user import User


class UsersRepo(BaseRepository):

    def __init__(self):
        super().__init__(User)

    async def get(
            self,
            session: AsyncSession,
            user_id: str
    ) -> User:
        user = await self.get_by(
            session,
            "user_id",
            user_id,
            unique=True
        )
        return user
