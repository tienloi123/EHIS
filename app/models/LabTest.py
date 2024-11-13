from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class LabTest(Base):
    __tablename__ = "lap_test"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=False)
    medical_record_id = Column(Integer, ForeignKey("medical_record.id", ondelete="CASCADE"), nullable=False)
    test_name = Column(String(), nullable=False)
    department = Column(String, nullable=False)
    test_date = Column(DateTime(timezone=True), nullable=False)
    result_test = Column(String, nullable=False)
    patient = relationship('User', foreign_keys=[patient_id], back_populates='lab_test_as_patient', lazy="selectin")
    doctor = relationship('User', foreign_keys=[doctor_id], back_populates='lab_test_as_doctor', lazy="selectin")
    def dict(self):
        result = self.to_dict()
        return result
