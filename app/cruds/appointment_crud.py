from typing import List

from sqlalchemy import select, asc, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import BaseCRUD
from app.cruds.base_crud import ModelType
from app.models.appointment import Appointment
from app.schemas import AppointmentCreate, AppointmentUpdate


class AppointmentCRUD(BaseCRUD[Appointment, AppointmentCreate, AppointmentUpdate]):
    async def get_all(
            self, session: AsyncSession, *args, **kwargs
    ) -> List[ModelType]:
        query = select(self._model)

        # Áp dụng điều kiện lọc nếu có trong `filter_rpn`
        if "filter_rpn" in kwargs:
            if len(kwargs["filter_rpn"]):
                condition = self.convert_filter_rpn_into_condition(kwargs["filter_rpn"])
                query = query.filter(condition)
            del kwargs["filter_rpn"]

        order = kwargs.pop('order', 'asc')
        query = query.filter(*args).filter_by(**kwargs)
        if order == 'desc':
            query = query.order_by(desc(self._model.created_at))
        else:
            query = query.order_by(asc(self._model.created_at))

        result = await session.execute(query)

        return result.scalars().all()


appointment_crud = AppointmentCRUD(Appointment)


