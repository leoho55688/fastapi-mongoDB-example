from typing import Callable, Optional

from fastapi import Depends, HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette import requests, status

from app.api.dependencies.database import get_collection
from app.core.config import get_app_setting
from app.core.setting import AppSettings
from app.db.errors import EntityDoesNotExist
from app.db.collections.users import UserCollection
from app.models.domain.users import User
from app.resources import strings
from app.services import jwt

HEADER_KEY = "Authorization"

class RWAPIKeyHeader(APIKeyHeader):
    async def __call__(self, request: requests.Request) -> Optional[str]:
        try:
            return await super().__call__(request)
        except StarletteHTTPException as original_auth_exc:
            raise HTTPException(
                status_code=original_auth_exc.status_code,
                detail=strings.AUTHENTICATION_REQUIRED,
            )
        
def _get_authorization_header_retriever(*, required: bool = True) -> Callable:
    return _get_authorization_header if required else _get_authorization_header_optional

def get_current_user_authorizer(*, required: bool = True) -> Callable:
    return _get_current_user if required else _get_current_user_optional

def _get_authorization_header(
    api_key: str = Security(RWAPIKeyHeader(name=HEADER_KEY)),
    settings: AppSettings = Depends(get_app_setting),
) -> str:
    try:
        token_prefix, token = api_key.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    if token_prefix != settings.jwt_token_prefix:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.WRONG_TOKEN_PREFIX,
        )
    
    return token

def _get_authorization_header_optional(
        authorization: Optional[str] = Security(
            RWAPIKeyHeader(name=HEADER_KEY, auto_error=False),
        ),
        settings: AppSettings = Depends(get_app_setting),
) -> str:
    if authorization:
        return _get_authorization_header(authorization, settings)
    
    return ""

async def _get_current_user(
    user_col: UserCollection = Depends(get_collection(UserCollection)),
    token: str = Depends(_get_authorization_header_retriever()),
    settings: AppSettings = Depends(get_app_setting),
) -> User:
    try:
        username = jwt.get_username_from_token(
            token,
            str(settings.secret_key.get_secret_value()),
        )
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )
    
    try:
        return await user_col.get_user_by_username(username=username)
    except EntityDoesNotExist:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=strings.MALFORMED_PAYLOAD,
        )
    
async def _get_current_user_optional(
    col: UserCollection = Depends(get_collection(UserCollection)),
    token: str = Depends(_get_authorization_header_retriever()),
    settings: AppSettings = Depends(get_app_setting),
) -> Optional[User]:
    if token:
        return await _get_current_user(col, token, settings)
    
    return None