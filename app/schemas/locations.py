from pydantic import BaseModel
from typing import List, Optional


from app.models.location import LocationCategory, AccessLevel


class LocationBase(BaseModel):
    id: int

    class Config:
        from_attributes = True


class Location(LocationBase):
    name: str
    lat: float
    long: float
    category: LocationCategory
    wheelchair_access: Optional[bool]
    accessible_toilet: Optional[bool]
    disabled_parking: Optional[bool]
    braille_signs: Optional[bool]
    induction_loops: Optional[bool]
    visual_audio_signals: Optional[bool]
    lowered_counters: Optional[bool]
    assistance_service: Optional[bool]
    guide_paths: Optional[bool]
    elevator: Optional[bool]
    seating_with_armrests: Optional[bool]

    hearing_access: AccessLevel
    wheelchair_access_level: AccessLevel
    vision_access_level: AccessLevel
    cognitive_access_level: AccessLevel


class LocationsResponse(BaseModel):
    locations: List[Location]

