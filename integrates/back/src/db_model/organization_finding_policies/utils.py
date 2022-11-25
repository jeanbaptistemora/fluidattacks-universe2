from .enums import (
    PolicyStateStatus,
)
from .types import (
    OrgFindingPolicy,
    OrgFindingPolicyState,
)
from datetime import (
    datetime,
    timezone,
)
from db_model import (
    TABLE,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Any,
)


def serialize(object_: Any) -> Any:
    if isinstance(object_, set):
        return list(object_)
    if isinstance(object_, datetime):
        return object_.astimezone(tz=timezone.utc).isoformat()
    return object_


def format_organization_finding_policy(
    item: Item,
) -> OrgFindingPolicy:
    key_structure = TABLE.primary_key
    return OrgFindingPolicy(
        id=item.get("id") or item[key_structure.partition_key].split("#")[1],
        name=item["name"],
        organization_name=item.get("organization_name")
        or item[key_structure.sort_key].split("#")[1],
        state=OrgFindingPolicyState(
            modified_by=item["state"]["modified_by"],
            modified_date=datetime.fromisoformat(
                item["state"]["modified_date"]
            ),
            status=PolicyStateStatus[item["state"]["status"]],
        ),
        tags=set(item["tags"]) if item.get("tags") else set(),
    )
