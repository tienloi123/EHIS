import logging
from abc import ABCMeta, abstractmethod
from enum import Enum
from typing import Sequence, List, Union

import httpx
from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import AppStatus
from app.constant.role_constant import RoleEnum
from app.core import settings, error_exception_handler
from app.models import User

logger = logging.getLogger(__name__)


class PermissionResult:
    def __init__(self, allow: bool, reasons: List[str] = None, filter_rpn: List[Union[str, dict]] = None):
        self.allow = allow
        self.reasons = reasons if reasons is not None else []
        self.filter_rpn = filter_rpn if filter_rpn is not None else []


class OpenPolicyAgentPermission(metaclass=ABCMeta):
    opa_url: str = None
    user_id: str = None
    role: RoleEnum = None
    scope: str = None
    metadata: {} = {}
    resource: Union[dict, List[dict]] = None

    class Scopes(Enum):
        CREATE = 'create'
        LIST = 'list'
        READ = 'read'
        UPDATE = 'update'
        DELETE = 'delete'

    def __init__(self, **kwargs):
        # kwargs include scope, user_id
        for name, val in kwargs.items():
            setattr(self, name, val)

        self.opa_url = f"http://{settings.OPA_SERVER}:{settings.OPA_SERVER_PORT}/v1/data"

        self.payload = {
            'input': {
                'scope': self.scope,
                'auth': {
                    'user': {
                        'id': self.user_id,
                        'role': self.role
                    }
                },
                'metadata': self.metadata,
                'resource': self.resource
            },
        }

    @classmethod
    @abstractmethod
    async def create(cls, request: Request, session: AsyncSession, user: Union[User, None]) -> Sequence[any]:
        ...

    @classmethod
    def create_base_perm(cls, **kwargs):
        return cls(**kwargs)

    @abstractmethod
    async def get_resource(self, **kwargs):
        return None

    async def check_access(self) -> PermissionResult:
        reasons = []

        async with httpx.AsyncClient() as session:
            response = await session.post(self.opa_url, json=self.payload)
            output = response.json().get('result', {})

        if isinstance(output, dict):
            allow = output.get('allow', False)
            reasons = output.get('reasons', [])
        elif isinstance(output, bool):
            allow = output
        else:
            raise error_exception_handler(app_status=AppStatus.ERROR_500_INTERNAL_SERVER_ERROR)
        return PermissionResult(allow=allow, reasons=reasons)

    async def filter(self):
        async with httpx.AsyncClient() as session:
            response = await session.post(self.opa_url.replace('/result', '/filter'), json=self.payload)
            filter_rpn = response.json().get('result', {})
        return PermissionResult(allow=True, filter_rpn=filter_rpn)
