from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
import hashlib
from typing import (
    Any,
)


def get_key(item: Item, key: str) -> Any:
    return item.get(key) or item.get("state", {}).get(key)


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=hashlib.sha256(item["sk"].encode("utf-8")).hexdigest(),
        attacked_at=datetime.fromisoformat(get_key(item, "attacked_at"))
        if get_key(item, "attacked_at")
        else None,
        attacked_by=get_key(item, "attacked_by"),
        be_present=bool(get_key(item, "be_present")),
        be_present_until=datetime.fromisoformat(
            get_key(item, "be_present_until")
        )
        if get_key(item, "be_present_until")
        else None,
        first_attack_at=datetime.fromisoformat(
            get_key(item, "first_attack_at")
        )
        if get_key(item, "first_attack_at")
        else None,
        group_name=item["group_name"],
        has_vulnerabilities=bool(get_key(item, "has_vulnerabilities")),
        root_id=get_key(item, "unreliable_root_id"),
        seen_at=datetime.fromisoformat(get_key(item, "seen_at"))
        if get_key(item, "seen_at")
        else None,
        seen_first_time_by=get_key(item, "seen_first_time_by"),
    )
