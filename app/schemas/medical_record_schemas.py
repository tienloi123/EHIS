from typing import Optional

from fastapi import UploadFile
from pydantic import BaseModel



class MedicalRecordCreate(BaseModel):
    patient_id: int
    doctor_id: int
    image: str

class MedicalRecordRequest(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_id: int
    file: Optional[UploadFile]
