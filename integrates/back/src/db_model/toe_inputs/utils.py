from .types import (
    ToeInput,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
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


def format_toe_input_item(
    primary_key: PrimaryKey,
    key_structure: PrimaryKey,
    toe_input: ToeInput,
) -> Item:
    return {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        "commit": toe_input.commit,
        "component": toe_input.component,
        "created_date": toe_input.created_date,
        "entry_point": toe_input.entry_point,
        "group_name": toe_input.group_name,
        "seen_first_time_by": toe_input.seen_first_time_by,
        "tested_date": toe_input.tested_date,
        "unreliable_root_id": toe_input.unreliable_root_id,
        "verified": toe_input.verified,
        "vulns": toe_input.vulns,
    }
