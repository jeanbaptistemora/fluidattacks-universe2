from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from typing import (
    Any,
)


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def serialize_sets(object_: Any) -> Any:
    if isinstance(object_, set):
        return list(object_)
    return object_
