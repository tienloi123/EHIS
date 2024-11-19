import logging
from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel
from sqlalchemy import Boolean

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
    doctor_id: Optional[int]
    start_time: Optional[datetime]
    end_time: Optional[datetime]
    status: Optional[StatusEnum]
    confirmed_by_doctor_id: Optional[int]
    medical_record: Optional[int]
    doctor_confirmed_status: Optional[bool]

class AppointmentUpdateRequest(BaseModel):
    doctor_id: int
    start_time: str
    end_time: str

class UpdateAppointmentNotification(BaseModel):
    _id: Optional[UUID]
    to_notify_users: Optional[List[int]]
    doctor_name: Optional[str]
    clinic_location: Optional[str]
    seen_users: Optional[List[int]]
    title: Optional[str]
    description: Optional[str]
    start_date: Optional[str]
    start_time: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

class CreatePaymentNotification(BaseModel):
    _id: Optional[UUID]
    to_notify_users: Optional[List[int]]
    receptionist_name: Optional[str]
    patient_name: Optional[str]
    status_payment:Optional[str]
    total_payment: Optional[str]
    seen_users: Optional[List[int]]
    title: Optional[str]
    description: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]