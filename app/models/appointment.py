from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Enum, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class Appointment(Base):
    __tablename__ = "appointment"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    description = Column(String(length=255), nullable=False)
    status = Column(Enum('UNPROCESSED', 'PROCESSED', name='status_appointment_enum'), nullable=False)
    start_time = Column(DateTime(timezone=True), nullable=True)
    end_time = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()),
                        onupdate=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    patient = relationship('User', foreign_keys=[patient_id], back_populates='appointments_as_patient', lazy="selectin")
    doctor = relationship('User', foreign_keys=[doctor_id], back_populates='appointments_as_doctor', lazy="selectin")
    def dict(self):
        result = self.to_dict()
        return result
