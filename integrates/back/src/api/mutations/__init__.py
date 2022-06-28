from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from typing import (
    NamedTuple,
)

AddOrganizationPayload = NamedTuple(
    "AddOrganizationPayload",
    [("success", bool), ("organization", Organization)],
)

GrantStakeholderAccessPayload = NamedTuple(
    "GrantStakeholderAccessPayload",
    [
        ("success", bool),
        ("granted_stakeholder", Stakeholder),
    ],
)
