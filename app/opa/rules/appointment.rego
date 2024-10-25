package appointment

import future.keywords.if
import future.keywords.contains
import data.utils

default allow = false

allow {
    utils.is_patient
    input.scope == utils.CREATE
}
reasons contains "Tài nguyên được yêu cầu thuộc về bệnh nhân" if {
    { utils.CREATE }[input.scope]
    input.scope == utils.CREATE
    not utils.is_patient
}

result := {
    "allow": allow,
    "reasons": reasons
}