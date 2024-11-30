import hashlib
import hmac
import json
import logging
import random
import time
from datetime import datetime, timedelta

import httpx
import requests
from fastapi import Depends, APIRouter, HTTPException, Request
from app.celery import send_notification_batch
from sqlalchemy.ext.asyncio import AsyncSession

from app.apis.depends.authorization import get_current_active_user, check_user_permissions
from app.constant import StatusPaymentEnum, COLLECTION_NAME
from app.constant.role_constant import RoleEnum
from app.core.exceptions import make_response_object
from app.cruds import payment_crud, user_crud, medical_record_crud
from app.database import get_async_session, db
from app.models import User, MedicalRecord
from app.models.Payment import Payment
from app.schemas import PaymentUpdate, PaymentRequest, UpdateAppointmentNotification
from app.services.payment_service import PaymentService

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("")
async def get_payments(status: str = None, offset: int = 0,
                       limit: int = 100, session: AsyncSession = Depends(get_async_session),
                       user: User = Depends(check_user_permissions),
                       ):
    payment_service = PaymentService(session=session)
    payment_data = await payment_service.get_payments(offset=offset, limit=limit, status=status)
    return make_response_object(data=payment_data)


@router.put("/{id}")
async def update_payment(id: int, session: AsyncSession = Depends(get_async_session),
                         user: User = Depends(get_current_active_user),
                         ):
    payment_service = PaymentService(session=session)
    payment_data = await payment_service.update_payment(id=id)
    return make_response_object(data=payment_data)


@router.get("/user")
async def user_get_payments(status: str = None, offset: int = 0,
                            limit: int = 100, session: AsyncSession = Depends(get_async_session),
                            user: User = Depends(get_current_active_user),
                            ):
    payment_service = PaymentService(session=session)
    payment_data = await payment_service.user_get_payments(offset=offset, limit=limit, status=status, user=user)
    return make_response_object(data=payment_data)

@router.post("/zalopay/create-payment")
async def create_zalopay_payment(payment: PaymentRequest):
    async with httpx.AsyncClient() as client:
        try:
            app_id = 2553
            key1 = "PcY4iZIKFCIdgZvA6ueMcMHHUbRLYjPL"
            endpoint = "https://sb-openapi.zalopay.vn/v2/create"
            transID = random.randrange(1000000)
            order = {
                "app_id": app_id,
                "app_trans_id": "{:%y%m%d}_{}".format(datetime.today(), transID),
                "app_user": f"{payment.payment_id}",
                "app_time": int(round(time.time() * 1000)),
                "embed_data": json.dumps({'redirecturl': 'http://localhost:3000/thanh-toan-thanh-cong'}),
                "item": json.dumps([{}]),
                "amount": int(payment.amount),
                "description": "Thanh toán tiền viện phí",
                "bank_code": "CC",
                "callback_url": 'https://7ee2-14-245-240-124.ngrok-free.app/api/payments/callback/',
            }
            mac_data = f"{order['app_id']}|{order['app_trans_id']}|{order['app_user']}|{order['amount']}|{order['app_time']}|{order['embed_data']}|{order['item']}"
            order["mac"] = hmac.new(key1.encode(), mac_data.encode(), hashlib.sha256).hexdigest()
            try:
                response = requests.post(endpoint, json=order)
                response.raise_for_status()
                response_data = response.json()
                if response_data.get('order_url'):
                    return {"zalopay_url": response_data['order_url']}
                else:
                    raise HTTPException(status_code=500, detail="Không nhận được URL từ ZaloPay")
            except requests.exceptions.RequestException as e:
                raise HTTPException(status_code=500, detail="Không thể kết nối đến API ZaloPay")
        except Exception as e:
            logger.exception(f"Exception occurred: {str(e)}")
            raise HTTPException(status_code=500, detail=str(e))
@router.post("/callback")
async def callback_zalopay(request: Request, session: AsyncSession = Depends(get_async_session)):
    try:
        body = await request.json()
        logger.info(f"Received callback with body: {body}")

        data = json.loads(body.get('data', '{}'))
        logger.info(f"Parsed data: {data}")

        amount = data.get("amount")
        payment_id = data.get("app_user")
        payment_id = int(payment_id)

        logger.info(f"Payment success: amount={amount}, payment_id={payment_id}")

        payment = await payment_crud.get(session, Payment.id == payment_id)
        if not payment:
            logger.error(f"Payment record not found for payment_id: {payment_id}")
            raise HTTPException(status_code=404, detail="Không tìm thấy thanh toán")

        payment_date = datetime.utcnow()

        payment_date_vn = payment_date + timedelta(hours=7)
        payment = await payment_crud.update(
            session,
            obj_in=PaymentUpdate(status=StatusPaymentEnum.COMPLETED, payment_date=payment_date_vn),
            db_obj=payment,
        )
        payment_amount = payment.amount
        medical_record_id = payment.medical_record_id
        medical_record = await medical_record_crud.get(session, MedicalRecord.id == medical_record_id )
        patient_name = medical_record.patient.name

        receptionist = await user_crud.get(session, User.role == RoleEnum.RECEPTIONIST)
        receptionist_id = receptionist.id
        notification_data = UpdateAppointmentNotification(to_notify_users=[receptionist_id],
                                                          seen_users=[],
                                                          title="Thông báo thanh toán thành công",
                                                          description=f"Thanh toán thành công số tiền: {payment_amount} từ bệnh nhân {patient_name}.",
                                                          created_at=datetime.now(),
                                                          updated_at=datetime.now(),
                                                          )
        notification_dict = notification_data.dict()
        user_ids = [receptionist_id]
        collection = db[COLLECTION_NAME]
        insert_result = collection.insert_one(notification_dict)
        notification_id = str(insert_result.inserted_id)
        notification_dict["_id"] = notification_id  # Thêm ID vào dữ liệu gửi đi
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)
        logger.info(f"Updated payment status to COMPLETED for payment_id: {payment_id}")
        return {"status": "success", "message": f"Thanh toán {payment_id} thành công: {amount}"}
    except Exception as e:
        logger.exception(f"Exception occurred while processing callback: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Lỗi khi xử lý callback: {str(e)}")



