from fastapi import APIRouter, Body, Depends, HTTPException
from starlette.status import HTTP_201_CREATED, HTTP_400_BAD_REQUEST

from app.api.dependencies.database import get_collection
from app.core.config import get_app_setting
from app.core.setting import AppSettings
from app.db.collections.users import UserCollection
from app.db.errors import EntityDoesNotExist
from app.models.domain.users import User
from app.models.schema.users import (
    UserInCreate,
    UserInResponse,
    UserInLogin,
    UserWithToken
)
from app.resources import strings
from app.services import jwt
from app.services.authentication import check_email_is_taken, check_username_is_taken

router = APIRouter()

@router.post(
    "/register",
    status_code=HTTP_201_CREATED,
    response_model=UserInResponse,
    name="auth:register",
)
async def register(
    user_create: UserInCreate = Body(..., embed=True, alias="user"),
    user_col: UserCollection = Depends(get_collection(UserCollection)),
    settings: AppSettings = Depends(get_app_setting),
) -> UserInResponse:
    if await check_username_is_taken(user_col, user_create.username):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.USERNAME_TAKEN
        )
    
    if await check_email_is_taken(user_col, user_create.email):
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=strings.EMAIL_TAKEN
        )
    
    user = await user_col.create_user(**user_create.model_dump())

    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value())
    )

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token
        )
    )

@router.post("/login", response_model=UserInResponse, name="auth:login")
async def login(
    user_login: UserInLogin = Body(..., embed=True, alias="user"),
    user_col: UserCollection = Depends(get_collection(UserCollection)),
    settings: AppSettings = Depends(get_app_setting),
) -> UserInResponse:
    wrong_login_error = HTTPException(
        status_code=HTTP_400_BAD_REQUEST,
        detail=strings.INCORRECT_LOGIN_INPUT
    )

    try:
        user = await user_col.get_user_by_email(email=user_login.email)
    except EntityDoesNotExist as existence_error:
        raise wrong_login_error from existence_error
    
    if not user.check_password(user_login.password):
        raise wrong_login_error
    
    token = jwt.create_access_token_for_user(
        user,
        str(settings.secret_key.get_secret_value())
    )

    return UserInResponse(
        user=UserWithToken(
            username=user.username,
            email=user.email,
            bio=user.bio,
            image=user.image,
            token=token
        )
    )
