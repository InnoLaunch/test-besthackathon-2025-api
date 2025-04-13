from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import Integer
from typing import Optional, List

from core.repository.base import BaseRepository
from app.models.location import Location, LocationCategory
from app.models.user import DisabilityType
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
import math


def haversine(lat1, lon1, lat2, lon2):
    return 6371 * func.acos(
        func.cos(func.radians(lat1)) * func.cos(func.radians(lat2)) *
        func.cos(func.radians(lon2) - func.radians(lon1)) +
        func.sin(func.radians(lat1)) * func.sin(func.radians(lat2))
    )


def get_accessibility_score(disability: DisabilityType):
    if disability == DisabilityType.WHEELCHAIR:
        return func.coalesce(Location.wheelchair_access.cast(Integer), 0) + \
               func.coalesce(Location.accessible_toilet.cast(Integer), 0)
    elif disability == DisabilityType.VISION:
        return func.coalesce(Location.braille_signs.cast(Integer), 0) + \
               func.coalesce(Location.guide_paths.cast(Integer), 0)
    elif disability == DisabilityType.HEARING:
        return func.coalesce(Location.induction_loops.cast(Integer), 0)
    elif disability == DisabilityType.COGNITIVE:
        return func.coalesce(Location.assistance_service.cast(Integer), 0)
    # Add more if needed
    return 0


class LocationsRepo(BaseRepository):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(session, Location)

    async def get_locations(
            self,
            disability: DisabilityType,
            category: LocationCategory,
            lat: Optional[float] = None,
            long: Optional[float] = None,
            offset: int = 0,
            limit: int = 100
    ) -> List[Location]:

        distance_expr = None
        if lat is not None and long is not None:
            distance_expr = haversine(lat, long, Location.lat, Location.long).label("distance")

        accessibility_score = get_accessibility_score(disability).label("accessibility_score")

        stmt = select(Location)
        if distance_expr is not None:
            stmt = stmt.add_columns(distance_expr)
        stmt = stmt.add_columns(accessibility_score)

        stmt = stmt.where(Location.category == category)

        if distance_expr is not None:
            stmt = stmt.order_by(distance_expr)
        stmt = stmt.order_by(desc(accessibility_score))

        stmt = stmt.offset(offset).limit(limit)

        return await self.all(stmt)

