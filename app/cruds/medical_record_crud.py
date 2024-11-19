from app.cruds import BaseCRUD
from app.schemas import MedicalRecordCreate
from app.models.MedicalRecords import MedicalRecord


class MedicalRecordCRUD(BaseCRUD[MedicalRecord, MedicalRecordCreate, MedicalRecordCreate]):
    pass


medical_record_crud = MedicalRecordCRUD(MedicalRecord)
