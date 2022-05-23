from db_model.organizations.types import (
    Organization,
)
from typing import (
    NamedTuple,
)

AddOrganizationPayload = NamedTuple(
    "AddOrganizationPayload",
    [("success", bool), ("organization", Organization)],
)
