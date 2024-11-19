from datetime import datetime

from pydantic import BaseModel



class LabTestCreate(BaseModel):
    medical_record_doctor_id: int
    test_name: str
    department: str
    result_test: str
    test_date: datetime


class LabTestRequest(BaseModel):
    medical_record_doctor_id: int
    test_name: str
    department: str
    result_test: str
