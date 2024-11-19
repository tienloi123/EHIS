import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.schemas import MedicalRecordRequest
from app.services.medical_record_service import MedicalService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('')
async def create_medical_record(medical_record_data: MedicalRecordRequest,
                 session: AsyncSession = Depends(get_async_session)):
    medical_record_service = MedicalService(session=session)
    medical_record_response = await medical_record_service.create_medical_record(medical_record_data=medical_record_data)
    return make_response_object(medical_record_response)
