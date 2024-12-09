import logging
from datetime import datetime
from itertools import groupby

from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery import send_notification_batch
from app.constant import StatusEnum, COLLECTION_NAME, StatusPaymentEnum
from app.constant.role_constant import RoleEnum
from app.cruds import appointment_crud, user_crud, medical_record_crud, medical_record_doctor_crud, payment_crud, \
    lab_test_crud
from app.database import db
from app.models import User, Appointment, MedicalRecord, LabTest
from app.models.medical_record_doctor import MedicalRecordDoctor
from app.schemas import AppointmentCreate, AppointmentRequest, AppointmentUpdateRequest, AppointmentUpdate, \
    UpdateAppointmentNotification, PaymentCreate, CreatePaymentNotification
from app.utils import convert_str_DMY_to_date_time, convert_datetime_to_date_str, \
    convert_datetime_to_time_str

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def report_appointments(self):
        appointments_data = [0, 0]
        appointments = await appointment_crud.get_all(session=self.session)

        for appointment in appointments:
            if appointment.status == StatusEnum.UNPROCESSED:
                appointments_data[0] += 1
            else:
                appointments_data[1] += 1

        return appointments_data

    async def round_report_appointments(self):
        appointments_data = [0, 0, 0]
        appointments = await appointment_crud.get_all(session=self.session)

        for appointment in appointments:
            appointments_data[0] += 1
            if appointment.status == StatusEnum.UNPROCESSED:
                appointments_data[1] += 1
            else:
                appointments_data[2] += 1

        return appointments_data

    async def user_create_appointment(self, appointment_data: AppointmentRequest, user_id):
        start_time = convert_str_DMY_to_date_time(date_str=appointment_data.start_time)
        appointment = await appointment_crud.create(session=self.session,
                                                    obj_in=AppointmentCreate(description=appointment_data.description,
                                                                             status=StatusEnum.UNPROCESSED,
                                                                             start_time=start_time, patient_id=user_id))
        user = await user_crud.get(self.session, User.id == user_id)
        user_name = user.name
        receptionist = await user_crud.get(self.session, User.role == RoleEnum.RECEPTIONIST)
        receptionist_id = receptionist.id
        receptionist_name = receptionist.name
        notification_data = UpdateAppointmentNotification(to_notify_users=[receptionist_id],
                                                          seen_users=[],
                                                          title="Thông báo mới từ bệnh nhân",
                                                          description=f"Bạn có 1 lịch hẹn mới từ bệnh nhân: {user_name}.",
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
        return appointment.dict()

    async def user_get_appointment(self, user: User, order: str = 'asc'):
        user_id = user.id
        appointments = await appointment_crud.get_all(
            session=self.session,
            patient_id=user_id,
            order=order
        )
        result = []

        for appointment in appointments:
            appointment_data = appointment.dict()
            if appointment.doctor_id:
                appointment_data['doctor_name'] = appointment.doctor.name
                appointment_data['doctor_clinic'] = appointment.doctor.clinic_location
            result.append(appointment_data)

        return result

    async def receptionist_get_appointment(self):
        appointments = await appointment_crud.get_all(self.session, Appointment.status == StatusEnum.UNPROCESSED)
        result = []

        for appointment in appointments:
            appointment_data = appointment.dict()
            if appointment.doctor_id:
                appointment_data['doctor_name'] = appointment.doctor.name
                appointment_data['doctor_clinic'] = appointment.doctor.clinic_location
            result.append(appointment_data)
        return result

    async def admin_get_appointment(self):
        appointments = await appointment_crud.get_all(self.session)
        result = []

        for appointment in appointments:
            appointment_data = appointment.dict()
            if appointment.doctor_id:
                appointment_data['doctor_name'] = appointment.doctor.name
                appointment_data['doctor_clinic'] = appointment.doctor.clinic_location
            result.append(appointment_data)
        return result

    async def me_get_doctor(self, user: User, department: str):
        # Lấy các bác sĩ không có `start_time` và không phải là chính mình
        doctors_with_no_start_time = await self.session.execute(
            select(User)
            .join(Appointment, Appointment.doctor_id == User.id, isouter=True)
            .where(
                User.department == department,
                Appointment.end_time == None,
                User.id != user.id  # Loại trừ chính mình
            )
        )
        doctors_with_no_start_time = doctors_with_no_start_time.scalars().all()

        result = []
        if doctors_with_no_start_time:
            for doctor in doctors_with_no_start_time:
                appointments = await appointment_crud.get_all(self.session, doctor_id=doctor.id)
                appointment_list = [appointment.to_dict() for appointment in appointments] if appointments else []

                # Gộp vào kết quả
                result.append({"doctor": doctor.to_dict(), "appointments": appointment_list})

            return result

        # Lấy các bác sĩ có `end_time` gần nhất và không phải là chính mình
        doctors_with_earliest_end_time = await self.session.execute(
            select(User, Appointment)
            .join(Appointment, Appointment.doctor_id == User.id)
            .where(
                User.department == department,
                User.id != user.id  # Loại trừ chính mình
            )
            .order_by(Appointment.end_time.asc(), User.id)
        )

        # Nhóm dữ liệu theo bác sĩ
        grouped_data = groupby(doctors_with_earliest_end_time.all(), key=lambda x: x[0].id)
        for doctor_id, appointments in grouped_data:
            appointments = list(appointments)
            doctor = appointments[0][0]  # Lấy thông tin bác sĩ từ phần tử đầu tiên
            appointment_list = [appointment[1].to_dict() for appointment in appointments]

            result.append({"doctor": doctor.to_dict(), "appointments": appointment_list})

        return result

    async def get_doctor(self, department: str):
        doctors_with_no_start_time = await self.session.execute(
            select(User)
            .join(Appointment, Appointment.doctor_id == User.id, isouter=True)
            .where(User.department == department, Appointment.end_time == None)
        )
        doctors_with_no_start_time = doctors_with_no_start_time.scalars().all()

        result = []
        if doctors_with_no_start_time:
            for doctor in doctors_with_no_start_time:
                appointments = await appointment_crud.get_all(self.session, doctor_id=doctor.id)
                appointment_list = [appointment.to_dict() for appointment in appointments] if appointments else []

                # Gộp vào kết quả
                result.append({"doctor": doctor.to_dict(), "appointments": appointment_list})

            return result

        doctors_with_earliest_end_time = await self.session.execute(
            select(User, Appointment)
            .join(Appointment, Appointment.doctor_id == User.id)
            .where(User.department == department)
            .order_by(Appointment.end_time.asc(), User.id)
        )

        grouped_data = groupby(doctors_with_earliest_end_time.all(), key=lambda x: x[0].id)
        for doctor_id, appointments in grouped_data:
            appointments = list(appointments)
            doctor = appointments[0][0]  # Lấy thông tin bác sĩ từ phần tử đầu tiên
            appointment_list = [appointment[1].to_dict() for appointment in appointments]

            result.append({"doctor": doctor.to_dict(), "appointments": appointment_list})

        return result

    async def update(self, appointment_data: AppointmentUpdateRequest, id: int):
        appointment = await appointment_crud.get(self.session, Appointment.id == id)
        start_time = convert_str_DMY_to_date_time(appointment_data.start_time)
        end_time = convert_str_DMY_to_date_time(appointment_data.end_time)
        data = await appointment_crud.update(self.session,
                                             obj_in=AppointmentUpdate(doctor_id=appointment_data.doctor_id,
                                                                      start_time=start_time,
                                                                      end_time=end_time,
                                                                      status=StatusEnum.PROCESSED,
                                                                      confirmed_by_doctor_id=appointment_data.doctor_id),
                                             db_obj=appointment)
        await self.session.refresh(data)
        return data

    async def doctor_update(self, appointment_data: AppointmentUpdateRequest, id: int):
        appointment = await appointment_crud.get(self.session, Appointment.id == id)
        start_time = convert_str_DMY_to_date_time(appointment_data.start_time)
        end_time = convert_str_DMY_to_date_time(appointment_data.end_time)
        data = await appointment_crud.update(self.session,
                                             obj_in=AppointmentUpdate(doctor_id=appointment_data.doctor_id,
                                                                      start_time=start_time,
                                                                      end_time=end_time),
                                             db_obj=appointment)
        await self.session.refresh(data)
        return data

    async def end(self, id: int):
        data_notification = {}
        total_amount_medical = 0
        appointment = await appointment_crud.get(self.session, Appointment.id == id)
        data = await appointment_crud.update(self.session, obj_in=AppointmentUpdate(doctor_confirmed_status=True),
                                             db_obj=appointment)
        medical_record = await medical_record_crud.get(self.session, MedicalRecord.id == data.medical_record)
        medical_record_doctors = await medical_record_doctor_crud.get_all(self.session,
                                                                          MedicalRecordDoctor.medical_record_id == medical_record.id)

        for medical_record_doctor in medical_record_doctors:
            total_amount_medical += medical_record_doctor.payment_amount
        payment = await payment_crud.create(self.session,
                                            obj_in=PaymentCreate(medical_record_id=medical_record.id,
                                                                 amount=total_amount_medical,
                                                                 status=StatusPaymentEnum.PENDING))
        receptionist = await user_crud.get(self.session, User.role == RoleEnum.RECEPTIONIST)

        receptionist_id = receptionist.id
        receptionist_name = receptionist.name
        patient_name = data.patient.name
        patient_id = data.patient.id
        total_payment = payment.amount
        status_payment = payment.status
        data_notification.update({"receptionist_name": receptionist_name, "patient_name": patient_name,
                                  "total_payment": str(total_payment), "status_payment": status_payment,
                                  "receptionist_id": receptionist_id, "patient_id": patient_id})
        return data_notification

    async def update_notification(self, data: Appointment, user):
        doctor_id = data.doctor_id
        patient_id = data.patient_id
        doctor_name = data.doctor.name
        clinic_location = data.doctor.clinic_location
        start_date = convert_datetime_to_date_str(data.start_time)
        start_time = convert_datetime_to_time_str(data.start_time)
        notification_data = UpdateAppointmentNotification(to_notify_users=[patient_id, doctor_id],
                                                          seen_users=[],
                                                          title="Thông báo lịch hẹn mới",
                                                          description=f"Bạn có 1 lịch hẹn mới. Lịch hẹn này được tạo tự động bởi lễ tân.",
                                                          doctor_name=doctor_name,
                                                          clinic_location=clinic_location,
                                                          start_date=start_date,
                                                          start_time=start_time,
                                                          created_at=datetime.now(),
                                                          updated_at=datetime.now(),
                                                          )
        notification_dict = notification_data.dict()
        user_ids = [patient_id, doctor_id]
        collection = db[COLLECTION_NAME]
        insert_result = collection.insert_one(notification_dict)
        notification_id = str(insert_result.inserted_id)
        notification_dict["_id"] = notification_id  # Thêm ID vào dữ liệu gửi đi
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)

    async def doctor_update_notification(self, data: Appointment, user):
        doctor_id = data.doctor_id
        patient_id = data.patient_id
        doctor_name = data.doctor.name
        clinic_location = data.doctor.clinic_location
        start_date = convert_datetime_to_date_str(data.start_time)
        start_time = convert_datetime_to_time_str(data.start_time)
        notification_data = UpdateAppointmentNotification(to_notify_users=[patient_id, doctor_id],
                                                          seen_users=[],
                                                          title="Thông báo lịch hẹn mới.",
                                                          description=f"Bạn có 1 lịch hẹn mới. Lịch hẹn này được tạo tự động bởi bác sĩ.",
                                                          doctor_name=doctor_name,
                                                          clinic_location=clinic_location,
                                                          start_date=start_date,
                                                          start_time=start_time,
                                                          created_at=datetime.now(),
                                                          updated_at=datetime.now(),
                                                          )
        notification_dict = notification_data.dict()
        user_ids = [patient_id, doctor_id]
        collection = db[COLLECTION_NAME]
        insert_result = collection.insert_one(notification_dict)
        notification_id = str(insert_result.inserted_id)
        notification_dict["_id"] = notification_id  # Thêm ID vào dữ liệu gửi đi
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)

    async def doctor_create_payment_notification(self, data: dict):
        receptionist_id = data.get('receptionist_id')
        patient_id = data.get('patient_id')
        receptionist_name = data.get('receptionist_name')
        status_payment = data.get('status_payment')
        patient_name = data.get('patient_name')
        total_payment = data.get('total_payment')
        notification_data = CreatePaymentNotification(to_notify_users=[patient_id, receptionist_id],
                                                      seen_users=[],
                                                      title="Thông báo thanh toán.",
                                                      description=f"Bạn có 1 thông báo thanh toán mới.",
                                                      receptionist_name=receptionist_name,
                                                      patient_name=patient_name,
                                                      created_at=datetime.now(),
                                                      updated_at=datetime.now(),
                                                      total_payment=total_payment,
                                                      status_payment=status_payment,
                                                      )
        notification_dict = notification_data.dict()
        user_ids = [patient_id, receptionist_id]
        collection = db[COLLECTION_NAME]
        insert_result = collection.insert_one(notification_dict)
        notification_id = str(insert_result.inserted_id)
        notification_dict["_id"] = notification_id  # Thêm ID vào dữ liệu gửi đi
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)

    async def doctor_get_appointment(self, user: User):
        appointments = await appointment_crud.get_all(self.session, and_(Appointment.doctor_confirmed_status == False,
                                                                         Appointment.doctor_id == user.id))
        result = []
        for appointment in appointments:
            appointment_data = appointment.dict()
            if appointment.patient_id:
                appointment_data['patient_name'] = appointment.patient.name
                appointment_data['patient_dob'] = appointment.patient.dob
            result.append(appointment_data)
        return result
