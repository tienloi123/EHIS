from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Enum, Date, BigInteger
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    email = Column(String(length=255), unique=True, nullable=False)
    name = Column(String(length=45), nullable=False)
    department = Column(String, nullable=False)
    dob = Column(Date, nullable=False)
    hashed_password = Column(String, nullable=False)
    clinic_location = Column(String, nullable=True)
    role = Column(Enum('Superuser', 'Doctor', 'Receptionist', 'Patient',name='role_enum'), nullable=False)
    gender = Column(Enum('Nam', 'Nữ', 'Khác', name='gender_enum'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    cccd_id = Column(BigInteger, nullable=True)
    residence = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()),
                        onupdate=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    appointments_as_patient = relationship('Appointment', foreign_keys='Appointment.patient_id',
                                           back_populates='patient', lazy="selectin")
    appointments_as_doctor = relationship('Appointment', foreign_keys='Appointment.doctor_id', back_populates='doctor',
                                          lazy="selectin")
    record_as_patient = relationship('MedicalRecord', foreign_keys='MedicalRecord.patient_id',
                                           back_populates='patient', lazy="selectin")
    record_as_doctor = relationship('MedicalRecord', foreign_keys='MedicalRecord.doctor_id', back_populates='doctor',
                                          lazy="selectin")
    otp = Column(String, nullable=True)
    def dict(self):
        result = self.to_dict(un_selects=['hashed_password','access_token','refresh_token'])
        return result
