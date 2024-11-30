from pydantic import BaseModel



class MedicalRecordDoctorCreate(BaseModel):
    medical_record_id: int
    diagnosis: str
    prescription: str
    payment_amount: float

class MedicalRecordDoctorRequest(BaseModel):
    appointment_id: int
    diagnosis: str
    prescription: str
    payment_amount: float
