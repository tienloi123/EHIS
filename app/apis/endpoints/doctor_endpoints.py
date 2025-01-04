import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import check_user_permissions
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.services.doctor_service import DoctorService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("")
async def get_doctors(offset: int = 0,
                      limit: int = 100, session: AsyncSession = Depends(get_async_session),
                      user: User = Depends(check_user_permissions),
                      ):
    doctor_service = DoctorService(session=session)
    doctor_data = await doctor_service.get_doctors(offset=offset, limit=limit)
    return make_response_object(data=doctor_data)
