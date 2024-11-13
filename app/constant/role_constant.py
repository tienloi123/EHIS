from enum import Enum


class RoleEnum(str, Enum):
    SUPERUSER = "Superuser"
    DOCTOR = "Doctor"
    RECEPTIONIST = "Receptionist"
    PATIENT = "Patient"