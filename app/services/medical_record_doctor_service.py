import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.cruds import medical_record_doctor_crud, appointment_crud
from app.models import Appointment
from app.schemas import MedicalRecordDoctorCreate, MedicalRecordDoctorRequest

logger = logging.getLogger(__name__)


class MedicalDoctorService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_medical_doctor_record(self, medical_record_doctor_data: MedicalRecordDoctorRequest):
        appointment = await appointment_crud.get(self.session, Appointment.id == medical_record_doctor_data.appointment_id)
        medical_record_data = await medical_record_doctor_crud.create(self.session, obj_in=MedicalRecordDoctorCreate(
            medical_record_id=appointment.medical_record,
            diagnosis=medical_record_doctor_data.diagnosis, prescription=medical_record_doctor_data.prescription,
            payment_amount=medical_record_doctor_data.payment_amount))

        return medical_record_data.dict()
