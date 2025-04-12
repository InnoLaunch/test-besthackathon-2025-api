from fastapi import APIRouter, Depends, Query
from typing import Optional

from app.schemas.locations import LocationsResponse
from app.controllers.locations import LocationsController
from app.models.user import DisabilityType
from app.models.location import LocationCategory


locations_rtr = APIRouter(tags=["Locations"])


@locations_rtr.get(path="/")
async def get_locations(
        locations_ctrl: LocationsController = Depends(),
        disability: DisabilityType = Query(),
        category: LocationCategory = Query(),
        lat: Optional[float] = Query(default=None),
        long: Optional[float] = Query(default=None),
        offset: int = Query(default=0),
        limit: int = Query(default=100),
) -> LocationsResponse:
    response = await locations_ctrl.get_locations(
        disability=disability,
        category=category,
        lat=lat,
        long=long,
        offset=offset,
        limit=limit
    )
    return LocationsResponse.model_validate(response)
