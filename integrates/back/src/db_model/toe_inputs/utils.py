from .types import (
    ToeInput,
)
from dynamodb.types import (
    Item,
)


def format_toe_input(
    *,
    group_name: str,
    item: Item,
) -> ToeInput:
    return ToeInput(
        commit=item["commit"],
        component=item["component"],
        created_date=item["created_date"],
        entry_point=item["entry_point"],
        group_name=group_name,
        seen_first_time_by=item["seen_first_time_by"],
        tested_date=item["tested_date"],
        unreliable_root_id=item.get("unreliable_root_id", ""),
        verified=item["verified"],
        vulns=item["vulns"],
    )
