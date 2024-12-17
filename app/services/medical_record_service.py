import logging
from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from app.celery import send_notification_batch
from app.constant import COLLECTION_NAME
from app.core import settings
from app.cruds import medical_record_crud, appointment_crud
from app.database import db
from app.models import Appointment
from app.schemas import MedicalRecordCreate, AppointmentUpdate, MedicalRecordRequest, UpdateAppointmentNotification
from app.utils.upload import get_minio_client, get_minio_bucket_name

logger = logging.getLogger(__name__)


class MedicalService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_medical_record(self, medical_record_data: MedicalRecordRequest):
        client = get_minio_client()
        bucket_name = get_minio_bucket_name()
        file_path = f"{settings.OBJECT_STORAGE_UPLOAD_MEDICAL_RECORD_FOLDER}/{medical_record_data.file.filename}"
        client.upload_fileobj(medical_record_data.file.file, bucket_name, file_path)

        # Tạo URL công khai để truy cập file
        file_url = f"{settings.OBJECT_STORAGE_ENDPOINT}/{bucket_name}/{file_path}"
        medical_record = await medical_record_crud.create(self.session, obj_in=MedicalRecordCreate(
            patient_id=medical_record_data.patient_id, doctor_id=medical_record_data.doctor_id, image=file_url))

        appointment = await appointment_crud.get(self.session, Appointment.id == medical_record_data.appointment_id)
        appointment_data = await appointment_crud.update(self.session,
                                                         obj_in=AppointmentUpdate(medical_record=medical_record.id),
                                                         db_obj=appointment)

        doctor_name = appointment_data.doctor.name
        patient_id = appointment_data.patient_id
        clinic_location = appointment_data.doctor.clinic_location
        medical_record_id = medical_record.id
        notification_data = UpdateAppointmentNotification(to_notify_users=[patient_id],
                                                          seen_users=[],
                                                          title="Thông báo tạo hồ sơ mới",
                                                          description=f"Bạn đã được Bác sĩ: {doctor_name} tạo hồ sơ mới với mã Hồ Sơ là: {medical_record_id}.",
                                                          clinic_location=clinic_location,
                                                          created_at=datetime.now(),
                                                          updated_at=datetime.now(),
                                                          )
        notification_dict = notification_data.dict()
        user_ids = [patient_id]
        collection = db[COLLECTION_NAME]
        insert_result = collection.insert_one(notification_dict)
        notification_id = str(insert_result.inserted_id)
        notification_dict["_id"] = notification_id  # Thêm ID vào dữ liệu gửi đi
        send_notification_batch.delay(channels=user_ids, notification_data=notification_dict)
        return medical_record_data.dict()
