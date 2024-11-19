from app.cruds import BaseCRUD
from app.models.medical_record_doctor import MedicalRecordDoctor
from app.schemas import MedicalRecordDoctorCreate


class MedicalRecordDoctorCRUD(BaseCRUD[MedicalRecordDoctor, MedicalRecordDoctorCreate, MedicalRecordDoctorCreate]):
    pass


medical_record_doctor_crud = MedicalRecordDoctorCRUD(MedicalRecordDoctor)
