import logging

from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import create_access_token, create_refresh_token
from app.constant import AppStatus
from app.core import error_exception_handler
from app.cruds import user_crud
from app.models import User
from app.schemas import AuthLogin, UserUpdate, OTP, PasswordReset, RegisterOtp, RegisterOTP
from app.utils import verify_password, generate_otp, send_email, hash_password

logger = logging.getLogger(__name__)


class AuthService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def login(self, auth_data: AuthLogin):
        user = await user_crud.get(self.session, User.email == auth_data.email)
        print(auth_data.email)
        if user is None:
            logger.error(AppStatus.ERROR_404_USER_NOT_FOUND.message,
                         exc_info=ValueError(AppStatus.ERROR_404_USER_NOT_FOUND))
            raise error_exception_handler(app_status=AppStatus.ERROR_404_USER_NOT_FOUND)
        if not user.is_active:
            logger.error(AppStatus.ERROR_403_USER_NOT_ACTIVE.message,
                         exc_info=ValueError(AppStatus.ERROR_403_USER_NOT_ACTIVE))
            raise error_exception_handler(app_status=AppStatus.ERROR_403_USER_NOT_ACTIVE)

        if not verify_password(password=auth_data.password,
                               hashed_password=user.hashed_password):
            logger.error(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD.message,
                         exc_info=ValueError(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD)

        data = {"user_id": user.id, "role": user.role}

        access_token = create_access_token(data=data)
        refresh_token = create_refresh_token(data=data)

        await user_crud.update(session=self.session,
                               obj_in=UserUpdate(access_token=access_token, refresh_token=refresh_token), db_obj=user)

        return {"access_token": access_token, "refresh_token": refresh_token, "full_name": user.name}

    async def logout(self, user):
        logger.info(f"logout called by {user.email}.")
        access_token = ""
        refresh_token = ""
        await user_crud.update(session=self.session, obj_in=UserUpdate(access_token=access_token,
                                                                       refresh_token=refresh_token), db_obj=user)
        logger.info(f"logout called successfully with access_token:{access_token}, refresh_token:{refresh_token}")
        return {"access_token": access_token, "refresh_token": refresh_token}

    async def send_otp(self, user):
        email = user.email
        otp = generate_otp()
        # Gửi email
        subject = "Mã OTP tạo mật khẩu mới của bạn"
        body = f"Chào bạn,\n\nMã OTP tạo mật khẩu mới của bạn là: {otp}\nMã này có hiệu lực trong 5 phút.\n\nBy EHIS"
        await send_email(to_email=email, subject=subject, body=body)
        await user_crud.update(self.session, obj_in=UserUpdate(otp=otp), db_obj=user)

        return {"otp_sent": True}

    async def verify_otp(self, user: User, otp_data: OTP):
        stored_otp = user.otp
        if stored_otp != otp_data.otp:
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_OTP)
        await user_crud.update(self.session, obj_in=UserUpdate(otp=''), db_obj=user)
        return {"verified": True}

    async def change_password(self, user: User, password_data: PasswordReset):
        if not verify_password(password=password_data.oldPassword, hashed_password=user.hashed_password):
            logger.error(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD.message,
                         exc_info=ValueError(AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD))
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_USERNAME_PASSWORD)
        hashed_password = hash_password(password_data.newPassword)
        await user_crud.update(session=self.session,
                               obj_in=UserUpdate(hashed_password=hashed_password), db_obj=user)

    async def register_send_otp(self, register_otp_data: RegisterOtp):
        user = await user_crud.get(self.session, User.id == register_otp_data.user_id)
        email = user.email
        otp = generate_otp()
        # Gửi email
        subject = "Mã OTP xác minh của bạn"
        body = f"Chào bạn,\n\nMã OTP tạo tài khoản mới của bạn là: {otp}\nMã này có hiệu lực trong 5 phút.\n\nBy EHIS"
        await send_email(to_email=email, subject=subject, body=body)
        await user_crud.update(self.session, obj_in=UserUpdate(otp=otp), db_obj=user)

        return {"otp_sent": True}

    async def register_verify_otp(self, otp_data: RegisterOTP):
        user = await user_crud.get(self.session, User.id == otp_data.user_id)
        stored_otp = user.otp
        if stored_otp != otp_data.otp:
            raise error_exception_handler(app_status=AppStatus.ERROR_400_INVALID_OTP)
        await user_crud.update(self.session, obj_in=UserUpdate(otp='', is_active=True), db_obj=user)
        return {"verified": True}
