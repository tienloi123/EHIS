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


class PaymentPermission(OpenPolicyAgentPermission):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.opa_url = self.opa_url + '/payments/result'

    @add_members_from(OpenPolicyAgentPermission.Scopes)
    class PaymentScopes(Enum):
        pass

    @classmethod
    async def create(cls, request: Request, session: AsyncSession, user: Union[User, None]) \
            -> List[OpenPolicyAgentPermission]:
        permissions = []
        if request.url.path.startswith(f'{BasePath}/payments') and request.method == "GET":
            self = cls.create_base_perm(scope=cls.PaymentScopes.READ.value, user_id=user.id,
                                        role=user.role)
            await self.get_resource(session=session)
            permissions.append(self)
        return permissions

    async def get_resource(self, session: AsyncSession, **kwargs):
        switch_scope = {
            self.PaymentScopes.CREATE.value: self.handle_create_scope,
            self.PaymentScopes.LIST.value: self.handle_list_scope,
            self.PaymentScopes.READ.value: self.handle_read_scope,
            self.PaymentScopes.UPDATE.value: self.handle_update_scope,
            self.PaymentScopes.DELETE.value: self.handle_delete_scope,
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
