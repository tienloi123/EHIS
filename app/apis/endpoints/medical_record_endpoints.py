import logging

from fastapi import Depends, APIRouter, Form, File, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.schemas import MedicalRecordRequest
from app.services.medical_record_service import MedicalService

router = APIRouter()
logger = logging.getLogger(__name__)

patient_id: int
doctor_id: int


@router.post('')
async def create_medical_record(appointment_id: int = Form(...),
                                file: UploadFile = File(...),
                                patient_id: int = Form(...),
                                doctor_id: int = Form(...),
                                session: AsyncSession = Depends(get_async_session),
                                user: User = Depends(get_current_active_user)
                                ):
    medical_record_data = MedicalRecordRequest(appointment_id=appointment_id, file=file, patient_id=patient_id,
                                               doctor_id=doctor_id)
    medical_record_service = MedicalService(session=session)
    medical_record_response = await medical_record_service.create_medical_record(
        medical_record_data=medical_record_data)
    return make_response_object(medical_record_response)
