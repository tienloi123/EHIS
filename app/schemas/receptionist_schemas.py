import logging
from datetime import datetime

from pydantic import BaseModel

from app.constant import StatusPaymentEnum

logger = logging.getLogger(__name__)


class ReceptionistCreate(BaseModel):
    pass


class ReceptionistUpdate(BaseModel):
    pass
