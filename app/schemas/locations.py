from pydantic import BaseModel
from typing import List


class LocationBase(BaseModel):
    id: int


class Location(LocationBase):
    pass


class LocationsResponse(BaseModel):
    locations: List[Location]

