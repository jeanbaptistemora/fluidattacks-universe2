from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
import hashlib


def format_row_metadata(
    item: Item,
) -> Item:
    state_item: Item = item["state"]

    return dict(
        id=hashlib.sha256(item["sk"].encode("utf-8")).hexdigest(),
        attacked_at=datetime.fromisoformat(state_item["attacked_at"])
        if state_item.get("attacked_at")
        else None,
        attacked_by=state_item.get("attacked_by"),
        be_present=bool(state_item.get("be_present")),
        be_present_until=datetime.fromisoformat(state_item["be_present_until"])
        if state_item.get("be_present_until")
        else None,
        first_attack_at=datetime.fromisoformat(state_item["first_attack_at"])
        if state_item.get("first_attack_at")
        else None,
        group_name=item["group_name"],
        has_vulnerabilities=bool(state_item.get("has_vulnerabilities")),
        root_id=state_item.get("unreliable_root_id"),
        seen_at=datetime.fromisoformat(state_item["seen_at"])
        if state_item.get("seen_at")
        else None,
        seen_first_time_by=state_item["seen_first_time_by"],
    )
