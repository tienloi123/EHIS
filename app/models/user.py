from sqlalchemy import Column, String, Boolean, DateTime, func, Integer, Enum
from sqlalchemy.orm import relationship

from . import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(length=255), unique=True, nullable=False)
    name = Column(String(length=45), nullable=False)
    dob = Column(DateTime(timezone=True), nullable=False)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum('Superuser', 'Docter', 'Receptionist', 'Patient',name='role_enum'), nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    updated_at = Column(DateTime(timezone=True), server_default=func.timezone('Asia/Ho_Chi_Minh', func.now()),
                        onupdate=func.timezone('Asia/Ho_Chi_Minh', func.now()))
    access_token = Column(String, nullable=True)
    refresh_token = Column(String, nullable=True)
    appointments_as_patient = relationship('Appointment', foreign_keys='Appointment.patient_id',
                                           back_populates='patient', lazy="selectin")
    appointments_as_doctor = relationship('Appointment', foreign_keys='Appointment.doctor_id', back_populates='doctor',
                                          lazy="selectin")
    def dict(self):
        result = self.to_dict(un_selects=['hashed_password','access_token','refresh_token'])
        return result
