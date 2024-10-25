import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import check_user_permissions
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.schemas import AppointmentRequest
from app.services.appointment_service import AppointmentService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("")
async def create_appointment(appointment_data: AppointmentRequest,
                      session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(check_user_permissions)):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.create_appointment(appointment_data=appointment_data)
    return make_response_object(data=appointment_data)
