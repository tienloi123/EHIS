import logging

from sqlalchemy.ext.asyncio import AsyncSession


from app.constant import AppStatus
from app.core import error_exception_handler
from app.cruds import user_crud
from app.models import User
from app.schemas import AuthLogin, UserUpdate
from app.utils import verify_password
from app.apis.depends.authorization import create_access_token, create_refresh_token

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, auth_data: AuthLogin):
        user = await user_crud.get(self.session, User.email == auth_data.email)

        if user is None:
            logger.error(AppStatus.ERROR_404_USER_NOT_FOUND.message,
                         exc_info=ValueError(AppStatus.ERROR_404_USER_NOT_FOUND))
            raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)

        if not verify_password(password=auth_data.password, hashed_password=user.hashed_password):
            logger.error(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD.message,
                         exc_info=ValueError(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD)

        data = {"user_id": user.id, "role": user.role}

        access_token = create_access_token(data=data)
        refresh_token = create_refresh_token(data=data)

        await user_crud.update(session=self.session,
                               obj_in=UserUpdate(access_token=access_token, refresh_token=refresh_token), db_obj=user)
        return {"access_token": access_token, "refresh_token": refresh_token}


    async def logout(self, user):
        logger.info(f"logout called by {user.email}.")
        access_token = ""
        refresh_token = ""
        await user_crud.update(session=self.session, obj_in=UserUpdate(access_token=access_token,
                                                                       refresh_token=refresh_token), db_obj=user)
        logger.info(f"logout called successfully with access_token:{access_token}, refresh_token:{refresh_token}")
        return {"access_token": access_token, "refresh_token": refresh_token}