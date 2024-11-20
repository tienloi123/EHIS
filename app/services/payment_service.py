import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from app.constant import StatusPaymentEnum
from app.cruds import payment_crud, user_crud, medical_record_crud, medical_record_doctor_crud, lab_test_crud
from app.models import User, MedicalRecord, LabTest
from app.models.Payment import Payment
from app.models.medical_record_doctor import MedicalRecordDoctor
from app.schemas import PaymentUpdate

logger = logging.getLogger(__name__)


class PaymentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def update_payment(self, id: int):
        payment = await payment_crud.get(self.session, Payment.id == id)
        payment_date = datetime.now()
        if payment:
            await payment_crud.update(self.session, obj_in=PaymentUpdate(status=StatusPaymentEnum.COMPLETED,
                                                                         payment_date=payment_date),
                                      db_obj=payment)
            return 'Success'

    async def get_payments(self, status, offset: int, limit: int):
        data = []
        # Tối ưu hóa truy vấn bằng cách sử dụng joinedload
        payments = await payment_crud.get_multi(
            self.session,
            status=status,
            offset=offset,
            limit=limit
        )
        for payment in payments:
            medical_record_id = payment.medical_record_id
            medical_record = await medical_record_crud.get(self.session, MedicalRecord.id == medical_record_id)
            doctor_name = medical_record.doctor.name
            patient_name = medical_record.patient.name

            medical_record_doctors_data = []

            medical_record_doctors = await medical_record_doctor_crud.get_all(
                self.session,
                MedicalRecordDoctor.medical_record_id == medical_record_id
            )

            for medical_record_doctor in medical_record_doctors:
                medical_record_doctor_data = {
                    "prescription": medical_record_doctor.prescription,
                    "diagnosis": medical_record_doctor.diagnosis,
                    "payment_amount": medical_record_doctor.payment_amount,
                }

                lab_test = await lab_test_crud.get(
                    self.session, LabTest.medical_record_doctor_id == medical_record_doctor.id
                )
                if lab_test:
                    medical_record_doctor_data.update({
                        "lab_test_name": lab_test.test_name,
                        "lab_test_result": lab_test.result_test,
                        "test_date": lab_test.test_date,
                    })

                medical_record_doctors_data.append(medical_record_doctor_data)

            data_detail = {
                "id": payment.id,
                "doctor_name": doctor_name,
                "patient_name": patient_name,
                "visit_date": payment.medical_record.visit_date,
                "payment_amount": payment.amount,
                "payment_status": payment.status,
                "payment_date": payment.payment_date,
                "medical_record_doctors": medical_record_doctors_data,  # Lưu danh sách đầy đủ
            }
            data.append(data_detail)
        return data
