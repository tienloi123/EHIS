import logging
from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.constant.role_constant import RoleEnum

logger = logging.getLogger(__name__)


class UserBase(BaseModel):
    email: str
    is_active: bool

    class Config:
        orm_mode = True


class UserCreate(UserBase):
    email: str
    hashed_password: str
    name: str
    dob: datetime
    role: RoleEnum


class UserRequest(BaseModel):
    email: str
    name: str
    dob: str
    password: str
    role: RoleEnum


class UserUpdate(UserBase):
    email: Optional[str] = None
    is_active: Optional[bool] = None
    role: Optional[str] = RoleEnum
    hashed_password: Optional[str] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class UserFilter(BaseModel):
    filtered_is_deleted: Optional[bool] = False
    filtered_delete_reason: Optional[str] = None


class UserDelete(BaseModel):
    pass