from pydantic import BaseModel



class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int

class MedicalRecordRequest(MedicalRecordCreate):
    appointment_id: int