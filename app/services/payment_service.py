import logging
from datetime import datetime

from sqlalchemy import and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.constant import StatusPaymentEnum
from app.cruds import payment_crud, medical_record_crud, medical_record_doctor_crud, lab_test_crud
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
    async def get_round_report_payments(self):
        payments_data = [0, 0, 0, 0]
        payments = await payment_crud.get_all(self.session)
        for payment in payments:
            payments_data[0] += 1
            if payment.status == StatusPaymentEnum.COMPLETED:
                payments_data[1] += 1
            elif payment.status == StatusPaymentEnum.PENDING:
                payments_data[2] += 1
            elif payment.status == StatusPaymentEnum.FAILED:
                payments_data[3] += 1
        return payments_data

    async def get_report_payments(self):
        payments = await payment_crud.get_all(self.session, and_(Payment.payment_date != None, Payment.status == StatusPaymentEnum.COMPLETED))
        payments_by_month = [0] * 12
        for payment in payments:
            month = payment.payment_date.month - 1
            payments_by_month[month] += payment.amount
        return payments_by_month

    async def get_payments(self, status, offset: int, limit: int):
        data = []
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
            patient_dob = medical_record.patient.dob
            patient_residence = medical_record.patient.residence
            patient_gender = medical_record.patient.gender
            patient_image = medical_record.image
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
                "patient_dob": patient_dob,
                "patient_residence": patient_residence,
                "patient_gender": patient_gender,
                "doctor_name": doctor_name,
                "patient_name": patient_name,
                "patient_image": patient_image,
                "visit_date": payment.medical_record.visit_date,
                "payment_amount": payment.amount,
                "payment_status": payment.status,
                "payment_date": payment.payment_date,
                "medical_record_doctors": medical_record_doctors_data,
            }
            data.append(data_detail)
        return data

    async def user_get_payments(self, status, offset: int, limit: int, user: User):
        data = []
        payments = await payment_crud.get_multi(
            self.session,
            status=status,
            offset=offset,
            limit=limit
        )
        for payment in payments:
            medical_record_id = payment.medical_record_id
            medical_record = await medical_record_crud.get(self.session, and_(MedicalRecord.id == medical_record_id,
                                                                              MedicalRecord.patient_id == user.id))
            if medical_record:
                later_medical_record_id = medical_record.id
                doctor_name = medical_record.doctor.name
                patient_name = medical_record.patient.name
                patient_dob = medical_record.patient.dob
                patient_gender = medical_record.patient.gender
                patient_residence = medical_record.patient.residence
                patient_image = medical_record.image

                medical_record_doctors_data = []

                medical_record_doctors = await medical_record_doctor_crud.get_all(
                    self.session,
                    MedicalRecordDoctor.medical_record_id == later_medical_record_id
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
                    "patient_residence": patient_residence,
                    "patient_dob": patient_dob,
                    "patient_gender": patient_gender,
                    "doctor_name": doctor_name,
                    "patient_name": patient_name,
                    "patient_image": patient_image,
                    "visit_date": payment.medical_record.visit_date,
                    "payment_amount": payment.amount,
                    "payment_status": payment.status,
                    "payment_date": payment.payment_date,
                    "medical_record_doctors": medical_record_doctors_data,
                }
                data.append(data_detail)
        return data
