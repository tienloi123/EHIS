import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import appointment_crud
from app.schemas import AppointmentCreate, AppointmentRequest
from app.utils import convert_str_DMY_to_date_time

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_appointment(self, appointment_data: AppointmentRequest):
        start_time = convert_str_DMY_to_date_time(date_str=appointment_data.start_time)
        end_time = convert_str_DMY_to_date_time(date_str=appointment_data.end_time)
        appointment = await appointment_crud.create(session=self.session, obj_in=AppointmentCreate(description=appointment_data.description,status=appointment_data.status,start_time=start_time,end_time=end_time))
        return  appointment.dict()
