import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import check_user_permissions, get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.schemas import AppointmentRequest, AppointmentUpdateRequest
from app.services.appointment_service import AppointmentService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("")
async def user_create_appointment(appointment_data: AppointmentRequest,
                                  session: AsyncSession = Depends(get_async_session),
                                  user: User = Depends(check_user_permissions)):
    appointment_service = AppointmentService(session=session)
    user_id = user.id
    appointment_data = await appointment_service.user_create_appointment(appointment_data=appointment_data,
                                                                         user_id=user_id)
    return make_response_object(data=appointment_data)


@router.get("")
async def user_get_appointment(session: AsyncSession = Depends(get_async_session),
                               user: User = Depends(get_current_active_user),
                               order: str = 'asc'  # Tham số mặc định
                               ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.user_get_appointment(user=user, order=order)
    return make_response_object(data=appointment_data)


@router.get("/for_receptionist")
async def receptionist_get_appointment(session: AsyncSession = Depends(get_async_session),
                                       user: User = Depends(get_current_active_user),
                                       ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.receptionist_get_appointment()
    return make_response_object(data=appointment_data)


@router.get("/doctors")
async def get_doctor(department: str, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(get_current_active_user),
                     ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.get_doctor(department=department)
    return make_response_object(data=appointment_data)
@router.get("/doctors/me")
async def me_get_doctor(department: str, session: AsyncSession = Depends(get_async_session),
                     user: User = Depends(get_current_active_user),
                     ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.me_get_doctor(department=department, user=user)
    return make_response_object(data=appointment_data)


@router.put("/{id}")
async def update(appointment_data: AppointmentUpdateRequest,
                 id: int, session: AsyncSession = Depends(get_async_session),
                 user: User = Depends(get_current_active_user),
                 ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.update(appointment_data=appointment_data, id=id)
    await appointment_service.update_notification(data=appointment_data, user=user)
    return make_response_object(data=appointment_data.dict())


@router.put("/end/{id}")
async def end(id: int, session: AsyncSession = Depends(get_async_session),
              user: User = Depends(get_current_active_user),
              ):
    appointment_service = AppointmentService(session=session)
    await appointment_service.end(id=id)
    return make_response_object(data='Success')


@router.get("/for_doctor")
async def doctor_get_appointment(session: AsyncSession = Depends(get_async_session),
                                 user: User = Depends(get_current_active_user),
                                 ):
    appointment_service = AppointmentService(session=session)
    appointment_data = await appointment_service.doctor_get_appointment(user=user)
    return make_response_object(data=appointment_data)
