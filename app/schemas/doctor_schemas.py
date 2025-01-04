import logging
from datetime import datetime

from pydantic import BaseModel

from app.constant import StatusPaymentEnum

logger = logging.getLogger(__name__)


class DoctorCreate(BaseModel):
    pass


class DoctorUpdate(BaseModel):
    pass
