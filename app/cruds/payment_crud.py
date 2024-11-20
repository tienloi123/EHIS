from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import BaseCRUD
from app.models.Payment import Payment
from app.schemas import PaymentCreate, PaymentUpdate


class PaymentCRUD(BaseCRUD[Payment, PaymentCreate, PaymentUpdate]):
    async def get_multi(self, session: AsyncSession,
                        *args,
                        offset: int = 0, limit: int = 100,
                        **kwargs):
        query = select(Payment)
        # Handle RPN filter condition
        if "filter_rpn" in kwargs and kwargs["filter_rpn"]:
            condition = self.convert_filter_rpn_into_condition(kwargs["filter_rpn"])
            query = query.filter(condition)
            del kwargs["filter_rpn"]

        for key, value in kwargs.items():
            if value is not None:  # Bỏ qua các giá trị None
                query = query.filter(getattr(Payment, key) == value)
        query = query.offset(offset).limit(limit)
        result = await session.execute(query)
        return result.scalars().all()


payment_crud = PaymentCRUD(Payment)
