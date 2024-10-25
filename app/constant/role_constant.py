from enum import Enum


class RoleEnum(str, Enum):
    SUPERUSER = "Superuser"
    DOCTER = "Docter"
    RECEPTIONIST = "Receptionist"
    PATIENT = "Patient"