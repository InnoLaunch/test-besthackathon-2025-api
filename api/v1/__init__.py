from fastapi import APIRouter

from api.v1.system import system_router
from api.v1.auth import auth_router


v1_router = APIRouter()
v1_router.include_router(system_router, prefix="/system")
v1_router.include_router(auth_router, prefix="/auth")
