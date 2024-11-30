package payments

import future.keywords.if
import future.keywords.contains
import data.utils

default allow = false

allow {
    utils.is_receptionist
    input.scope == utils.READ
}
reasons contains "Tài nguyên được yêu cầu thuộc về lễ tân" if {
    { utils.READ }[input.scope]
    input.scope == utils.READ
    not utils.is_receptionist
}

result := {
    "allow": allow,
    "reasons": reasons
}