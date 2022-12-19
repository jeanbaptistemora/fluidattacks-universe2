from .types import (
    ToeInput,
    ToeInputEdge,
    ToeInputState,
)
from datetime import (
    datetime,
)
from db_model import (
    utils as db_model_utils,
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
from typing import (
    Optional,
)


def format_toe_input(
    group_name: str,
    item: Item,
) -> ToeInput:
    state = item.get("state", {})
    return ToeInput(
        state=ToeInputState(
            attacked_at=datetime.fromisoformat(
                state.get("attacked_at", item.get("attacked_at"))
            )
            if state.get("attacked_at") or item.get("attacked_at")
            else None,
            attacked_by=state.get("attacked_by", item.get("attacked_by", "")),
            be_present=state.get("be_present", item.get("be_present", True)),
            be_present_until=datetime.fromisoformat(
                state.get("be_present_until", item.get("be_present_until"))
            )
            if state.get("be_present_until") or item.get("be_present_until")
            else None,
            first_attack_at=datetime.fromisoformat(
                state.get("first_attack_at", item.get("first_attack_at"))
            )
            if state.get("first_attack_at") or item.get("first_attack_at")
            else None,
            has_vulnerabilities=state.get(
                "has_vulnerabilities", item.get("has_vulnerabilities")
            ),
            modified_by=state.get("modified_by"),
            modified_date=datetime.fromisoformat(state["modified_date"])
            if state.get("modified_date")
            else None,
            seen_at=datetime.fromisoformat(
                state.get("seen_at", item.get("seen_at"))
            )
            if state.get("seen_at") or item.get("seen_at")
            else None,
            seen_first_time_by=state["seen_first_time_by"]
            if state.get("seen_first_time_by")
            else item["seen_first_time_by"],
            unreliable_root_id=state.get(
                "unreliable_root_id", item.get("unreliable_root_id", "")
            ),
        ),
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
        has_vulnerabilities=item.get("has_vulnerabilities"),
        seen_at=datetime.fromisoformat(item["seen_at"])
        if item.get("seen_at")
        else None,
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
        else db_model_utils.get_as_utc_iso_format(toe_input.attacked_at),
        "attacked_by": toe_input.attacked_by,
        "be_present": toe_input.be_present,
        "be_present_until": ""
        if toe_input.be_present_until is None
        else db_model_utils.get_as_utc_iso_format(toe_input.be_present_until),
        "component": toe_input.component,
        "entry_point": toe_input.entry_point,
        "first_attack_at": ""
        if toe_input.first_attack_at is None
        else db_model_utils.get_as_utc_iso_format(toe_input.first_attack_at),
        "has_vulnerabilities": toe_input.has_vulnerabilities,
        "group_name": toe_input.group_name,
        "seen_at": ""
        if toe_input.seen_at is None
        else db_model_utils.get_as_utc_iso_format(toe_input.seen_at),
        "seen_first_time_by": toe_input.seen_first_time_by,
        "unreliable_root_id": toe_input.unreliable_root_id,
        "state": {
            "modified_by": toe_input.state.modified_by,
            "modified_date": get_as_utc_iso_format(
                toe_input.state.modified_date
            )
            if toe_input.state.modified_date
            else "",
        },
    }
