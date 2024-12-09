import logging

from fastapi import Depends, APIRouter
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get('/profile')
async def get_me(
        user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)):
    data = user.dict()
    return make_response_object(data)
