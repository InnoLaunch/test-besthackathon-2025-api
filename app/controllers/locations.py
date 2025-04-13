from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from typing import (
    Dict,
    Tuple,
    List,
    Optional
)
from typing import Any

from core.controller.base import BaseController
from core.exceptions.base import UnauthorizedException
from core.database.session import get_session
from app.repositories.locations import LocationsRepo
from app.models.user import DisabilityType
from app.models.location import Location, LocationCategory
from core.exceptions.base import ConflictException
from core.security.password import PasswordHandler
from core.security.jwthandler import (JWTHandler, TokenType)


class LocationsController(BaseController):

    def __init__(self, session: AsyncSession = Depends(get_session)):
        super().__init__(session)
        self.repo = LocationsRepo(session)

    async def get_locations(
            self,
            disability: DisabilityType,
            category: LocationCategory,
            lat: Optional[float] = None,
            long: Optional[float] = None,
            offset: int = 0,
            limit: int = 100
    ) -> Dict[str, Any]:
        locations = await self.repo.get_locations(
            disability=disability,
            category=category,
            lat=lat,
            long=long,
            offset=offset,
            limit=limit
        )
        response = {}
        response["locations"] = locations
        return response
