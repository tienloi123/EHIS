from sqlalchemy import Column, Integer, String, Float

from . import Base


class MedicalRecordDoctor(Base):
    __tablename__ = "medical_record_doctor"

    id = Column(Integer, primary_key=True)
    medical_record_id = Column(Integer, nullable=False)  # ID của bản ghi khám
    diagnosis = Column(String, nullable=True)  # Chẩn đoán
    prescription = Column(String, nullable=True)  # Đơn thuốc
    payment_amount = Column(Float, nullable=True)  # Số tiền thanh toán

    def dict(self):
        result = self.to_dict()
        return result