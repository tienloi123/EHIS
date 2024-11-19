import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.schemas import LabTestRequest
from app.services.lab_test_service import LabTestService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('')
async def create_lab_test(lab_test_data: LabTestRequest,
                 session: AsyncSession = Depends(get_async_session)):
    lab_test_service = LabTestService(session=session)
    lab_test_response = await lab_test_service.create_lab_test(lab_test_data=lab_test_data)
    return make_response_object(lab_test_response)
