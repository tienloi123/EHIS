import logging

from fastapi import APIRouter, UploadFile, File, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models.user import User
from app.services.user_service import UserService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/profile')
async def get_me(
        user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)):
    data = user.dict()
    return make_response_object(data)


@router.post("/upload-avatar")
async def upload_avatar(user: User = Depends(get_current_active_user), file: UploadFile = File(...),
                        session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session=session)
    data = await user_service.upload_avatar(user=user, file=file)
    return make_response_object({"avatar": data})
