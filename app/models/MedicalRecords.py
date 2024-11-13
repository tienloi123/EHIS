from sqlalchemy import Column, String, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class MedicalRecord(Base):
    __tablename__ = "medical_record"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    appointment_id = Column(Integer, ForeignKey("appointment.id", ondelete="CASCADE"), nullable=True)
    diagnosis = Column(String, nullable=True)
    prescription = Column(String, nullable=True)
    visit_date = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    notes = Column(String, nullable=True)
    patient = relationship('User', foreign_keys=[patient_id], back_populates='record_as_patient', lazy="selectin")
    doctor = relationship('User', foreign_keys=[doctor_id], back_populates='record_as_doctor', lazy="selectin")
    appointment = relationship('Appointment', back_populates='medical_record')

    def dict(self):
        result = self.to_dict()
        return result
