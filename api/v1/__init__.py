from fastapi import APIRouter

from api.v1.system import system_router
from api.v1.auth import auth_router
from api.v1.locations import locations_rtr


v1_router = APIRouter()
v1_router.include_router(system_router, prefix="/system")
v1_router.include_router(auth_router, prefix="/auth")
v1_router.include_router(locations_rtr, prefix="/locations")
