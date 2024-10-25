from app.cruds import BaseCRUD
from app.models.appointment import Appointment
from app.schemas import AppointmentCreate, AppointmentUpdate


class AppointmentCRUD(BaseCRUD[Appointment, AppointmentCreate, AppointmentUpdate]):
    pass


appointment_crud = AppointmentCRUD(Appointment)
