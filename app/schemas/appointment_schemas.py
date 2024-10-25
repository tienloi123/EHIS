import logging
from datetime import datetime

from pydantic import BaseModel

from app.constant import StatusEnum

logger = logging.getLogger(__name__)

class AppointmentBase(BaseModel):
    description: str
    status: StatusEnum

class AppointmentCreate(AppointmentBase):
    start_time: datetime
    end_time: datetime

class AppointmentRequest(AppointmentBase):
    start_time: str
    end_time: str

class AppointmentUpdate(BaseModel):
    patient_id: int
    doctor_id: int
