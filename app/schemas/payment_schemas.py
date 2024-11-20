import logging
from datetime import datetime

from pydantic import BaseModel

from app.constant import StatusPaymentEnum

logger = logging.getLogger(__name__)


class PaymentCreate(BaseModel):
    medical_record_id: int
    amount: float
    status: StatusPaymentEnum

class PaymentUpdate(BaseModel):
    status: StatusPaymentEnum
    payment_date: datetime
