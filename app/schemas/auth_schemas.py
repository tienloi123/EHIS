from typing import List

from pydantic import BaseModel


class AuthBase(BaseModel):
    email: str
    password: str

    class Config:
        orm_mode = True


class AuthLogin(AuthBase):
    pass


class AuthCookieLogin(AuthBase):
    pass

class AuthLoginFace(BaseModel):
    images: List[str]

class Face(AuthLoginFace):
    pass