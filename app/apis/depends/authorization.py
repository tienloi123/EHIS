import logging
from datetime import datetime, timedelta
from typing import List, Union

import jwt
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import AppStatus
from app.constant.auth_constants import ACCESS_TOKEN_EXPIRES_IN_SECONDS, REFRESH_TOKEN_EXPIRES_IN_SECONDS, JWT_ALGORITHM
from app.core import settings, error_exception_handler
from app.database import get_async_session
from app.models import User
from app.opa.permissions.base_permission import OpenPolicyAgentPermission
from app.services.user_service import UserService
from app.utils.misc import create_bullet_list

logger = logging.getLogger(__name__)


def create_token(data: dict, token_type: str, expired_at=None):
    to_encode = data.copy()
    created_at = datetime.utcnow().timestamp()
    if token_type == "access":
        expired_at = datetime.utcnow() + timedelta(seconds=ACCESS_TOKEN_EXPIRES_IN_SECONDS)
    else:
        expired_at = datetime.utcfromtimestamp(expired_at) if expired_at is not None \
            else datetime.utcnow() + timedelta(seconds=REFRESH_TOKEN_EXPIRES_IN_SECONDS)
    to_encode.update({"token_type": token_type, "exp": expired_at, "created_at": created_at})

    encoded_jwt = jwt.encode(to_encode, settings.JWT_SECRET, algorithm=JWT_ALGORITHM)

    return encoded_jwt


def create_access_token(data: dict):
    return create_token(data, token_type="access")


def create_refresh_token(data: dict, expired_at=None):
    return create_token(data, token_type="refresh", expired_at=expired_at)


async def verify_token(token: str, session: AsyncSession):
    if not token:
        logger.error(AppStatus.ERROR_400_INVALID_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_400_INVALID_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_TOKEN)

    try:
        decoded_token = jwt.decode(token,
                                   settings.JWT_SECRET,
                                   algorithms=JWT_ALGORITHM)
    except jwt.exceptions.ExpiredSignatureError:
        logger.error(AppStatus.ERROR_401_EXPIRED_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_401_EXPIRED_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_401_EXPIRED_TOKEN)
    except jwt.exceptions.InvalidSignatureError:
        logger.error(AppStatus.ERROR_400_INVALID_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_400_INVALID_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_TOKEN)
    except jwt.exceptions.DecodeError:
        logger.error(AppStatus.ERROR_400_INVALID_TOKEN.message, exc_info=ValueError(AppStatus.ERROR_400_INVALID_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_TOKEN)
    # check user existence
    user_id = decoded_token['user_id']
    user_service = UserService(session=session)
    user = await user_service.get_one_by_id(user_id=user_id)
    token_type = decoded_token['token_type']
    if (token_type == "access" and user.access_token != token) or (token_type == "refresh" and user.refresh_token != token):
        logger.error(AppStatus.ERROR_401_EXPIRED_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_401_EXPIRED_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_401_EXPIRED_TOKEN)

    return decoded_token


async def verify_access_token(
        token: str,
        session: AsyncSession,
):
    decoded_token = await verify_token(token, session)
    if decoded_token['token_type'] != "access":
        logger.error(AppStatus.ERROR_400_INVALID_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_400_INVALID_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_TOKEN)
    return decoded_token


async def verify_refresh_token(
        token: str,
        session: AsyncSession,
):
    decoded_token = await verify_token(token, session)
    if decoded_token['token_type'] != "refresh":
        logger.error(AppStatus.ERROR_400_INVALID_TOKEN.message,
                     exc_info=ValueError(AppStatus.ERROR_400_INVALID_TOKEN))
        raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_TOKEN)
    return decoded_token


async def get_current_active_user(
        request: Request,
        credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer(auto_error=False)),
        session: AsyncSession = Depends(get_async_session)
):
    token = None
    if request.cookies.get("access_token", None):
        token = request.cookies["access_token"]
    elif credentials:
        token = credentials.credentials
    user_decode = await verify_access_token(token=token, session=session)
    user_id = user_decode['user_id']
    user_service = UserService(session=session)
    user = await user_service.get_one_by_id(user_id=user_id)

    if not user.is_active:
        logger.error(AppStatus.HTTP_401_USER_NOT_ACTIVE.message,
                     exc_info=ValueError(AppStatus.HTTP_401_USER_NOT_ACTIVE))
        raise error_exception_handler(app_status=AppStatus.HTTP_401_USER_NOT_ACTIVE)

    return user


async def gather_permissions(request: Request, user: User, session: AsyncSession) -> List[OpenPolicyAgentPermission]:
    permissions = []
    for perm_class in OpenPolicyAgentPermission.__subclasses__():
        permissions.extend(await perm_class.create(request=request, user=user, session=session))
    return permissions


async def check_permissions(permissions: List[OpenPolicyAgentPermission]):
    allow = True
    reasons = []

    for perm in permissions:
        result = await perm.check_access()
        reasons.extend(result.reasons)
        allow &= result.allow
    if not allow:
        if len(reasons):
            raise error_exception_handler(app_status=AppStatus.ERROR_405_METHOD_NOT_ALLOWED_BY_OPA,
                                          description=create_bullet_list(reasons))
        else:
            raise error_exception_handler(app_status=AppStatus.ERROR_405_METHOD_NOT_ALLOWED)

    return allow


async def filter_by_user_permissions(request: Request, user: User = Depends(get_current_active_user),
                                     session: AsyncSession = Depends(get_async_session)) -> List[Union[dict, str]]:
    user_permissions = await gather_permissions(request=request, user=user, session=session)

    filter_rpn = []

    for perm in user_permissions:
        if perm.payload['input']['scope'] == 'list':
            result = await perm.filter()
            if len(filter_rpn):
                filter_rpn.extend(result.filter_rpn.extend(['&']))
            else:
                filter_rpn.extend(result.filter_rpn)

    return filter_rpn


async def check_user_permissions(request: Request, session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(get_current_active_user)):
    user_permissions = await gather_permissions(request=request, session=session, user=user)
    await check_permissions(user_permissions)
    return user
