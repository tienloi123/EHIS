import logging

from fastapi import Depends, APIRouter, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user
from app.constant.auth_constants import ACCESS_TOKEN_EXPIRES_IN_SECONDS, REFRESH_TOKEN_EXPIRES_IN_SECONDS
from app.core.exceptions import make_response_object
from app.database import get_async_session
from app.models import User
from app.schemas import AuthLogin, UserRequest, OTP, PasswordReset, RegisterOtp, RegisterOTP
from app.services.auth_service import AuthService
from app.services.user_service import UserService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post('/bearer-jwt/login')
async def login_bearer(auth_data: AuthLogin, response: Response, session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session=session)
    auth_response = await auth_service.login(auth_data=auth_data)
    access_token = auth_response.get("access_token")
    refresh_token = auth_response.get("refresh_token")
    response.set_cookie(key="access_token", value=access_token, max_age=ACCESS_TOKEN_EXPIRES_IN_SECONDS,
                        httponly=True)
    response.set_cookie(key="refresh_token", value=refresh_token, max_age=REFRESH_TOKEN_EXPIRES_IN_SECONDS,
                        httponly=True)
    return make_response_object({**auth_response, "token_type": "cookie"})


@router.get('/bearer-jwt/logout')
async def logout_bearer(user: User = Depends(get_current_active_user),
                        session: AsyncSession = Depends(get_async_session)):
    auth_service = AuthService(session=session)
    await auth_service.logout(user=user)
    return make_response_object("Đăng xuất thành công")


@router.post("/register")
async def register(user_data: UserRequest,
                   session: AsyncSession = Depends(get_async_session)):
    user_service = UserService(session=session)
    user_data = await user_service.register(user_data=user_data)
    return make_response_object(data=user_data)


@router.post('/send-otp')
async def send_otp(user: User = Depends(get_current_active_user),
                   session: AsyncSession = Depends(get_async_session)):
    try:
        auth_service = AuthService(session)
        response = await auth_service.send_otp(user=user)
        return {"message": "OTP đã được gửi thành công", **response}
    except Exception as e:
        return {"message": f"Lỗi khi gửi OTP: {str(e)}", "otp_sent": False}


@router.post('/register-send-otp')
async def register_send_otp(register_otp_data: RegisterOtp,
                            session: AsyncSession = Depends(get_async_session)):
    try:
        auth_service = AuthService(session)
        response = await auth_service.register_send_otp(register_otp_data=register_otp_data)
        return {"message": "OTP đã được gửi thành công", **response}
    except Exception as e:
        return {"message": f"Lỗi khi gửi OTP: {str(e)}", "otp_sent": False}


@router.post('/verify-otp')
async def verify_otp(
        otp_data: OTP,
        user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    auth_service = AuthService(session)
    response = await auth_service.verify_otp(user=user, otp_data=otp_data)
    return {"message": "OTP đã được xác thực thành công", "verified": True, **response}


@router.post('/change-password')
async def change_password(
        password_data: PasswordReset,
        user: User = Depends(get_current_active_user),
        session: AsyncSession = Depends(get_async_session)
):
    auth_service = AuthService(session)
    await auth_service.change_password(user=user, password_data=password_data)  # Verify OTP, not send it
    return make_response_object(data='success')


@router.post('/register-verify-otp')
async def register_verify_otp(
        otp_data: RegisterOTP,  # OTP provided by the user
        session: AsyncSession = Depends(get_async_session)
):
    auth_service = AuthService(session)
    response = await auth_service.register_verify_otp(otp_data=otp_data)  # Verify OTP, not send it
    return {"message": "OTP đã được xác thực thành công", "verified": True, **response}
