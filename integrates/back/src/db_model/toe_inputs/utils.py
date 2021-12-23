from .types import (
    ToeInput,
    ToeInputEdge,
)
from datetime import (
    datetime,
    timezone,
)
from db_model import (
    utils as db_model_utils,
)
from dynamodb.types import (
    Index,
    Item,
    PrimaryKey,
    Table,
)
from dynamodb.utils import (
    get_cursor,
)
from typing import (
    Optional,
)


def format_toe_input(
    group_name: str,
    item: Item,
) -> ToeInput:
    return ToeInput(
        attacked_at=datetime.fromisoformat(item["attacked_at"])
        if item.get("attacked_at")
        else None,
        attacked_by=item.get("attacked_by", ""),
        be_present=item.get("be_present", True),
        be_present_until=datetime.fromisoformat(item["be_present_until"])
        if item.get("be_present_until")
        else None,
        component=item["component"],
        entry_point=item["entry_point"],
        first_attack_at=datetime.fromisoformat(item["first_attack_at"])
        if item.get("first_attack_at")
        else None,
        group_name=group_name,
        seen_at=datetime.fromisoformat(
            item.get("seen_at", datetime.now(tz=timezone.utc).isoformat()),
        ),
        seen_first_time_by=item["seen_first_time_by"],
        unreliable_root_id=item.get("unreliable_root_id", ""),
    )


def format_toe_input_edge(
    group_name: str,
    index: Optional[Index],
    item: Item,
    table: Table,
) -> ToeInputEdge:
    return ToeInputEdge(
        node=format_toe_input(group_name, item),
        cursor=get_cursor(index, item, table),
    )


def format_toe_input_item(
    primary_key: PrimaryKey,
    key_structure: PrimaryKey,
    gsi_2_key: PrimaryKey,
    gsi_2_index: Index,
    toe_input: ToeInput,
) -> Item:
    return {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        "attacked_at": ""
        if toe_input.attacked_at is None
        else db_model_utils.get_date_as_utc_iso_format(toe_input.attacked_at),
        "attacked_by": toe_input.attacked_by,
        "be_present": toe_input.be_present,
        "be_present_until": ""
        if toe_input.be_present_until is None
        else db_model_utils.get_date_as_utc_iso_format(
            toe_input.be_present_until
        ),
        "component": toe_input.component,
        "entry_point": toe_input.entry_point,
        "first_attack_at": ""
        if toe_input.first_attack_at is None
        else db_model_utils.get_date_as_utc_iso_format(
            toe_input.first_attack_at
        ),
        "group_name": toe_input.group_name,
        "seen_at": db_model_utils.get_date_as_utc_iso_format(
            toe_input.seen_at
        ),
        "seen_first_time_by": toe_input.seen_first_time_by,
        "unreliable_root_id": toe_input.unreliable_root_id,
    }
