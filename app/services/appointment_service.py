import logging
from datetime import datetime
from itertools import groupby

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.celery import send_notification_batch
from app.constant import StatusEnum, COLLECTION_NAME
from app.cruds import appointment_crud
from app.database import db
from app.models import User, Appointment
from app.schemas import AppointmentCreate, AppointmentRequest, AppointmentUpdateRequest, AppointmentUpdate, \
    UpdateAppointmentNotification
from app.utils import convert_str_DMY_to_date_time, convert_datetime_to_str, convert_datetime_to_date_str, \
    convert_datetime_to_time_str

logger = logging.getLogger(__name__)


class AppointmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def user_create_appointment(self, appointment_data: AppointmentRequest, user_id):
        start_time = convert_str_DMY_to_date_time(date_str=appointment_data.start_time)
        appointment = await appointment_crud.create(session=self.session,
                                                    obj_in=AppointmentCreate(description=appointment_data.description,
                                                                             status=StatusEnum.UNPROCESSED,
                                                                             start_time=start_time, patient_id=user_id))
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
                                                                      status=StatusEnum.UNPROCESSED),
                                             db_obj=appointment)
        await self.session.refresh(data)
        return data

    async def update_notification(self, data:Appointment, user):
        doctor_id = data.doctor_id
        patient_id = data.patient_id
        doctor_name = data.doctor.name
        receptionist_name = user.name
        clinic_location = data.doctor.clinic_location
        start_date = convert_datetime_to_date_str(data.start_time)
        start_time = convert_datetime_to_time_str(data.start_time)
        print(start_time)
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
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)
        collection = db[COLLECTION_NAME]
        collection.insert_one(notification_dict)
