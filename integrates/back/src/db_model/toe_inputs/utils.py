from .types import (
    ToeInput,
    ToeInputEdge,
    ToeInputMetadataToUpdate,
    ToeInputState,
)
from datetime import (
    datetime,
)
from db_model.utils import (
    get_as_utc_iso_format,
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


def format_toe_input(
    group_name: str,
    item: Item,
) -> ToeInput:
    state_item: Item = item["state"]
    return ToeInput(
        state=ToeInputState(
            attacked_at=datetime.fromisoformat(state_item["attacked_at"])
            if state_item.get("attacked_at")
            else None,
            attacked_by=state_item.get("attacked_by", ""),
            be_present=state_item.get("be_present", True),
            be_present_until=datetime.fromisoformat(
                state_item["be_present_until"]
            )
            if state_item.get("be_present_until")
            else None,
            first_attack_at=datetime.fromisoformat(
                state_item["first_attack_at"]
            )
            if state_item.get("first_attack_at")
            else None,
            has_vulnerabilities=state_item.get("has_vulnerabilities"),
            modified_by=state_item["modified_by"],
            modified_date=datetime.fromisoformat(state_item["modified_date"]),
            seen_at=datetime.fromisoformat(state_item["seen_at"])
            if state_item.get("seen_at")
            else None,
            seen_first_time_by=state_item["seen_first_time_by"],
            unreliable_root_id=state_item.get("unreliable_root_id", ""),
        ),
        component=item["component"],
        entry_point=item["entry_point"],
        group_name=group_name,
    )


def format_toe_input_edge(
    group_name: str,
    index: Index | None,
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
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        "component": toe_input.component,
        "entry_point": toe_input.entry_point,
        "group_name": toe_input.group_name,
        "state": {
            "attacked_at": get_as_utc_iso_format(toe_input.state.attacked_at)
            if toe_input.state.attacked_at
            else None,
            "attacked_by": toe_input.state.attacked_by,
            "be_present": toe_input.state.be_present,
            "be_present_until": get_as_utc_iso_format(
                toe_input.state.be_present_until
            )
            if toe_input.state.be_present_until
            else None,
            "first_attack_at": get_as_utc_iso_format(
                toe_input.state.first_attack_at
            )
            if toe_input.state.first_attack_at
            else None,
            "has_vulnerabilities": toe_input.state.has_vulnerabilities,
            "modified_by": toe_input.state.modified_by,
            "modified_date": get_as_utc_iso_format(
                toe_input.state.modified_date
            ),
            "seen_at": get_as_utc_iso_format(toe_input.state.seen_at)
            if toe_input.state.seen_at
            else None,
            "seen_first_time_by": toe_input.state.seen_first_time_by,
            "unreliable_root_id": toe_input.state.unreliable_root_id,
        },
    }


def format_toe_input_state_item(
    state_item: Item, metadata: ToeInputMetadataToUpdate
) -> Item:
    if metadata.clean_attacked_at:
        state_item["attacked_at"] = None
    if metadata.clean_be_present_until:
        state_item["be_present_until"] = None
    if metadata.clean_first_attack_at:
        state_item["first_attack_at"] = None
    if metadata.clean_seen_at:
        state_item["seen_at"] = None

    return state_item
