import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.services.payment_service import PaymentService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("")
async def get_payments(status: str = None, offset: int = 0,
                       limit: int = 100, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(get_current_active_user),
                       ):
    payment_service = PaymentService(session=session)
    payment_data = await payment_service.get_payments(offset=offset, limit=limit, status=status)
    return make_response_object(data=payment_data)


@router.put("/{id}")
async def update_payment(id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(get_current_active_user),
                         ):
    payment_service = PaymentService(session=session)
    payment_data = await payment_service.update_payment(id=id)
    return make_response_object(data=payment_data)
