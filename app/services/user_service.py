import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import AppStatus
from app.core import error_exception_handler, settings
from app.cruds import user_crud
from app.models import User
from app.schemas import UserCreate, UserRequest, UserUpdate
from app.utils import hash_password, convert_str_DMY_to_date
from app.utils.upload import get_minio_client, get_minio_bucket_name

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
        email = await user_crud.get(self.session, User.email == user_data.email)
        hashed_password = hash_password(user_data.password)
        if user:
            logger.error(AppStatus.ERROR_400_USER_ALREADY_EXISTS.message,
                         exc_info=ValueError(AppStatus.ERROR_400_USER_ALREADY_EXISTS))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_USER_ALREADY_EXISTS)
        elif email:
            logger.error(AppStatus.ERROR_400_EMAIL_ALREADY_EXISTS.message,
                         exc_info=ValueError(AppStatus.ERROR_400_USER_ALREADY_EXISTS))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_EMAIL_ALREADY_EXISTS)
        dob = convert_str_DMY_to_date(date_str=user_data.dob)
        data = await user_crud.create(session=self.session, obj_in=UserCreate(email=user_data.email, is_active=False,
                                                                              hashed_password=hashed_password,
                                                                              role=user_data.role,
                                                                              gender=user_data.gender, dob=dob,
                                                                              name=user_data.name,
                                                                              department=user_data.department,
                                                                              clinic_location=user_data.clinic_location,
                                                                              cccd_id=user_data.cccd_id,
                                                                              residence=user_data.residence))
        return data.dict()

    async def upload_avatar(self, user, file):
        client = get_minio_client()
        bucket_name = get_minio_bucket_name()
        file_path = f"{settings.OBJECT_STORAGE_UPLOAD_ME_FOLDER}/{file.filename}"
        client.upload_fileobj(file.file, bucket_name, file_path)

        # Tạo URL công khai để truy cập file
        file_url = f"{settings.OBJECT_STORAGE_ENDPOINT}/{bucket_name}/{file_path}"
        await user_crud.update(self.session, obj_in=UserUpdate(avatar_url=file_url), db_obj=user)
        return str(file_url)

