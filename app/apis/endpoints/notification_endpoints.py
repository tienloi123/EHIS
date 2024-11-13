import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.services.notification_service import NotificationService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/get_all')
async def get_notification(user: User = Depends(get_current_active_user),
                           session: AsyncSession = Depends(get_async_session)):
    notification_service = NotificationService(session=session)
    data = await notification_service.get_notification(user_id=user.id)
    return make_response_object(data)

@router.put('/mark-as-read/{notification_id}')
async def mark_as_read(notification_id: str, user: User = Depends(get_current_active_user),
                       session: AsyncSession = Depends(get_async_session)):
    notification_service = NotificationService(session=session)
    data = await notification_service.mark_as_read(user_id=user.id, notification_id=notification_id)
    return make_response_object(data)

@router.put('/mark-all-as-read')
async def mark_all_as_read(user: User = Depends(get_current_active_user),
                           session: AsyncSession = Depends(get_async_session)):
    notification_service = NotificationService(session=session)
    data = await notification_service.mark_all_as_read(user_id=user.id)
    return make_response_object(data)

@router.get('/message-unread')
async def get_notification_unseen(user: User = Depends(get_current_active_user),
                           session: AsyncSession = Depends(get_async_session)):
    notification_service = NotificationService(session=session)
    data = await notification_service.get_notification_unseen(user_id=user.id)
    return make_response_object(data)