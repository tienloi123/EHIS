import logging
from enum import Enum
from typing import Union, List

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import BasePath
from app.models import User
from app.opa.permissions.base_permission import OpenPolicyAgentPermission
from app.utils.decorator import add_members_from

logger = logging.getLogger(__name__)


class AppointmentPermission(OpenPolicyAgentPermission):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opa_url = self.opa_url + '/appointment/result'

    @add_members_from(OpenPolicyAgentPermission.Scopes)
    class AppointmentScopes(Enum):
        pass

    @classmethod
    async def create(cls, request: Request, session: AsyncSession, user: Union[User, None]) \
            -> List[OpenPolicyAgentPermission]:
        permissions = []
        if request.url.path.startswith(f'{BasePath}/appointment') and request.method == "POST":
            self = cls.create_base_perm(scope=cls.AppointmentScopes.CREATE.value, user_id=user.id,
                                        role=user.role)
            await self.get_resource(session=session)
            permissions.append(self)
        return permissions

    async def get_resource(self, session: AsyncSession, **kwargs):
        switch_scope = {
            self.AppointmentScopes.CREATE.value: self.handle_create_scope,
            self.AppointmentScopes.LIST.value: self.handle_list_scope,
            self.AppointmentScopes.READ.value: self.handle_read_scope,
            self.AppointmentScopes.UPDATE.value: self.handle_update_scope,
            self.AppointmentScopes.DELETE.value: self.handle_delete_scope,
        }

        handler = switch_scope.get(self.scope)
        await handler(session=session, **kwargs)

    async def handle_create_scope(self, session: AsyncSession, **kwargs):
        pass

    async def handle_list_scope(self, session: AsyncSession, **kwargs):
        pass

    async def handle_read_scope(self, session: AsyncSession, **kwargs):
        pass

    async def handle_update_scope(self, session: AsyncSession, **kwargs):
        pass

    async def handle_delete_scope(self, session: AsyncSession, **kwargs):
        pass
