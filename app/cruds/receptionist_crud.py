from typing import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant.role_constant import RoleEnum
from app.cruds import BaseCRUD
from app.models import User
from app.models.Payment import Payment
from app.schemas import ReceptionistCreate, ReceptionistUpdate


class ReceptionistCRUD(BaseCRUD[User, ReceptionistCreate, ReceptionistUpdate]):
    async def get_multi(self, session: AsyncSession,
                        *args,
                        offset: int = 0, limit: int = 100,
                        **kwargs) -> Sequence[User]:
        query = select(User)
        # Handle RPN filter condition
        if "filter_rpn" in kwargs and kwargs["filter_rpn"]:
            condition = self.convert_filter_rpn_into_condition(kwargs["filter_rpn"])
            query = query.filter(condition)
            del kwargs["filter_rpn"]

        for key, value in kwargs.items():
            if value is not None:  # Bỏ qua các giá trị None
                query = query.filter(getattr(Payment, key) == value)
        query = query.offset(offset).limit(limit)
        query = query.filter(User.role == RoleEnum.RECEPTIONIST)
        result = await session.execute(query)
        return result.scalars().all()


receptionist_crud = ReceptionistCRUD(User)
