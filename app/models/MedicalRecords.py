from sqlalchemy import Column, DateTime, func, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class MedicalRecord(Base):
    __tablename__ = "medical_record"
    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    doctor_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), nullable=True)
    visit_date = Column(DateTime(timezone=True),
                        server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()))  # Ngày khám bệnh

    # Quan hệ với bảng User
    patient = relationship('User', foreign_keys=[patient_id], back_populates='record_as_patient', lazy="selectin")
    doctor = relationship('User', foreign_keys=[doctor_id], back_populates='record_as_doctor', lazy="selectin")
    payments = relationship("Payment", back_populates="medical_record", cascade="all, delete-orphan")
    def dict(self):
        result = self.to_dict()
        return result
