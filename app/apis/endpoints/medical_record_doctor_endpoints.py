import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.schemas import MedicalRecordDoctorRequest
from app.services.medical_record_doctor_service import MedicalDoctorService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('')
async def create_medical_record_doctor(medical_record_doctor_data: MedicalRecordDoctorRequest,
                 session: AsyncSession = Depends(get_async_session)):
    medical_record_doctor_service = MedicalDoctorService(session=session)
    medical_record_doctor_response = await medical_record_doctor_service.create_medical_doctor_record(medical_record_doctor_data=medical_record_doctor_data)
    return make_response_object(medical_record_doctor_response)
