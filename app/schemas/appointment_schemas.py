import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel

from app.constant import StatusEnum

logger = logging.getLogger(__name__)

class AppointmentBase(BaseModel):
    description: str

class AppointmentCreate(AppointmentBase):
    patient_id: int
    status: StatusEnum
    start_time: datetime

class AppointmentRequest(AppointmentBase):
    start_time: str

class AppointmentUpdate(BaseModel):
    doctor_id: int
    start_time: datetime
    end_time: datetime
    status: StatusEnum
class AppointmentUpdateRequest(BaseModel):
    doctor_id: int
    start_time: str
    end_time: str

class UpdateAppointmentNotification(BaseModel):
    _id: Optional[UUID]
    to_notify_users: List[int]
    doctor_name: str
    clinic_location: str
    seen_users: List[int]
    title: str
    description: str
    start_date: str
    start_time: str
    created_at: datetime
    updated_at: datetime