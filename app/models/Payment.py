from sqlalchemy import Column, Integer, Float, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from . import Base


class Payment(Base):
    __tablename__ = 'payment'

    id = Column(Integer, primary_key=True, index=True)
    medical_record_id = Column(Integer, ForeignKey('medical_record.id', ondelete="SET NULL"), nullable=True)
    amount = Column(Float, nullable=False)
    status = Column(Enum('PENDING', 'COMPLETED', 'FAILED', name='status_payment_enum'), nullable=False, default='PENDING')
    payment_date = Column(DateTime(timezone=True), default=datetime.now)

    # Quan hệ với bảng MedicalRecord
    medical_record = relationship("MedicalRecord", back_populates="payments")
