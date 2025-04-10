from sqlalchemy.ext.asyncio import AsyncSession

from core.repository.base import BaseRepository
from app.models.user import User


class UsersRepo(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, User)

    async def get(
            self,
            user_id: str
    ) -> User:
        user = await self.get_by(
            "user_id",
            user_id,
            unique=True
        )
        return user
