from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from fastapi import Depends
from fastapi import Response

from app.schemas.auth import Token
from app.schemas.users import (
    User,
    SignupUser
)
from app.controllers.auth import AuthCtrl
from app.dependencies.users import (
    get_current_user,
    get_user_by_refresh,
    get_admin
)
from app.models.user import User as UserModel
from core.security.jwthandler import JWTHandler


auth_router = APIRouter(tags=["Auth"])


@auth_router.post(
    path="/token",
    description="OAuth2 compatible token generation. Used for logging user in",
)
async def token(
        fa_response: Response,
        form_data: OAuth2PasswordRequestForm = Depends(),
        auth_ctrl: AuthCtrl = Depends()
) -> Token:
    response, refresh_token = await auth_ctrl.token(
        username=form_data.username,
        password=form_data.password
    )
    fa_response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        max_age=int(JWTHandler.expire_refresh.total_seconds()),
        secure=True,
        samesite='none'
    )
    return Token(**response)


@auth_router.get(
    path="/refresh",
    description="OAuth2 refresh token",
)
async def refresh(
        auth_ctrl: AuthCtrl = Depends(),
        user: UserModel = Depends(get_user_by_refresh)
) -> Token:
    response = await auth_ctrl.refresh(
        user_id=user.user_id
    )
    return Token(**response)


@auth_router.post(
    path="/signup",
    description="Endpoint for creating new user. Requires admin privileges"
)
async def signup(
        signup_user: SignupUser,
        auth_ctrl: AuthCtrl = Depends()
) -> User:
    response = await auth_ctrl.signup(
        username=signup_user.username,
        password=signup_user.password
    )
    return User.model_validate(response)


@auth_router.get(
    path="/getme"
)
async def get_me(
        user: UserModel = Depends(get_current_user)
) -> User:
    return User.model_validate(user)
