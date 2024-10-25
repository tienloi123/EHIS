package utils
import future.keywords.in

# Scopes
CREATE := "create"
RETRIEVE := "retrieve"
LIST := "list"
UPDATE := "update"
DELETE := "destroy"

# Groups
SUPERUSER := "Superuser"
DOCTER := "Docter"
RECEPTIONIST := "Receptionist"
PATIENT := "Patient"

DATA_NULL := "None"

is_superuser {
    input.auth.user.role == SUPERUSER
}

is_doctor {
    input.auth.user.role == DOCTER
}

is_receptionist {
    input.auth.user.role == RECEPTIONIST
}

is_patient {
    input.auth.user.role == PATIENT
}