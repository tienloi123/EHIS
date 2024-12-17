package payments

import future.keywords.if
import future.keywords.contains
import data.utils

default allow = false

allow {
    utils.is_receptionist
    input.scope == utils.READ
}
allow {
    utils.is_superuser
    input.scope == utils.READ
}
allow {
    utils.is_doctor
    input.scope == utils.READ
}
reasons contains "Tài nguyên được yêu cầu thuộc về quản lý bệnh viện và lễ tân và bác sĩ" if {
    { utils.READ }[input.scope]
    not utils.is_receptionist
    not utils.is_doctor
    not utils.is_superuser
}

result := {
    "allow": allow,
    "reasons": reasons
}