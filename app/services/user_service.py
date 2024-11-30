import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import AppStatus
from app.core import error_exception_handler
from app.cruds import user_crud
from app.models import User
from app.schemas import UserCreate, UserRequest
from app.utils import hash_password, convert_str_DMY_to_date

logger = logging.getLogger(__name__)


class UserService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_one_by_id(self, user_id: int):
        user = await user_crud.get(self.session, User.id == user_id)
        if user is None:
            logger.error(AppStatus.ERROR_404_USER_NOT_FOUND.message,
                         exc_info=ValueError(AppStatus.ERROR_404_USER_NOT_FOUND))
            raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)
        return user

    async def register(self, user_data: UserRequest):
        user = await user_crud.get(self.session, User.cccd_id == user_data.cccd_id)
        hashed_password = hash_password(user_data.password)
        if user:
            logger.error(AppStatus.ERROR_400_USER_ALREADY_EXISTS.message,
                         exc_info=ValueError(AppStatus.ERROR_400_USER_ALREADY_EXISTS))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_USER_ALREADY_EXISTS)
        dob = convert_str_DMY_to_date(date_str=user_data.dob)
        data = await user_crud.create(session=self.session, obj_in=UserCreate(email=user_data.email, is_active=True,
                                                                              hashed_password=hashed_password,
                                                                              role=user_data.role,
                                                                              gender=user_data.gender, dob=dob,
                                                                              name=user_data.name,
                                                                              department=user_data.department,
                                                                              clinic_location=user_data.clinic_location,
                                                                              cccd_id=user_data.cccd_id,
                                                                              residence=user_data.residence))
        return data.dict()
