from sqlalchemy import Column
from sqlalchemy import (
    Integer,
    String,
    Float,
    Boolean,
    Enum as SAEnum
)
from enum import Enum

from core.database.base import Base


class LocationCategory(str, Enum):
    UNKNOWN = "unknown"
    HOSPITAL = "hospital"
    PHARMACY = "pharmacy"
    PARK = "park"
    MUSEUM = "museum"
    HOTEL = "hotel"
    BANK = "bank"
    FUEL = "fuel"
    ENTERTAINMENT = "entertainment"
    FOODMARKET = "foodmarket"
    RESTAURANT = "restaurant"
    POSTOFFICE = "postoffice"
    ELECTRICSHOP = "electricshop"


class AccessLevel(str, Enum):
    unknown = "unknown"
    no_access = "no_access"
    partial = "partial"
    full = "full"


class Location(Base):

    __tablename__ = 'locations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    lat = Column(Float, nullable=False)
    long = Column(Float, nullable=False)
    category = Column(
        SAEnum(LocationCategory, name="location_category"),
        nullable=False,
        default=LocationCategory.UNKNOWN
    )

    wheelchair_access = Column(Boolean)
    accessible_toilet = Column(Boolean)
    disabled_parking = Column(Boolean)
    braille_signs = Column(Boolean)
    induction_loops = Column(Boolean)
    visual_audio_signals = Column(Boolean)
    lowered_counters = Column(Boolean)
    assistance_service = Column(Boolean)
    guide_paths = Column(Boolean)
    elevator = Column(Boolean)
    seating_with_armrests = Column(Boolean)

    # Property to calculate hearing access level
    @property
    def hearing_access(self) -> AccessLevel:
        # Consider tags related to hearing (e.g., induction loops, visual/audio signals)
        if self.induction_loops and self.visual_audio_signals:
            return AccessLevel.full
        elif self.induction_loops or self.visual_audio_signals:
            return AccessLevel.partial
        return AccessLevel.no_access

    # Property to calculate wheelchair access level
    @property
    def wheelchair_access_level(self) -> AccessLevel:
        # Consider wheelchair access facilities (e.g., ramps, accessible toilets)
        if self.wheelchair_access and self.accessible_toilet and self.elevator:
            return AccessLevel.full
        elif self.wheelchair_access or self.accessible_toilet:
            return AccessLevel.partial
        return AccessLevel.no_access

    # Property to calculate vision access level
    @property
    def vision_access_level(self) -> AccessLevel:
        # Consider vision access facilities (e.g., braille signs, guide paths)
        if self.braille_signs and self.guide_paths:
            return AccessLevel.full
        elif self.braille_signs or self.guide_paths:
            return AccessLevel.partial
        return AccessLevel.no_access

    # Property to calculate cognitive access level (you can define what that means in your case)
    @property
    def cognitive_access_level(self) -> AccessLevel:
        # You can adjust this according to specific accessibility needs
        if self.assistance_service:
            return AccessLevel.full
        return AccessLevel.no_access


