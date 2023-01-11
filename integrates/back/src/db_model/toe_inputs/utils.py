from .types import (
    ToeInput,
    ToeInputEdge,
    ToeInputMetadataToUpdate,
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
    serialize,
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
import simplejson as json
from typing import (
    Optional,
)


def format_toe_input(
    group_name: str,
    item: Item,
) -> ToeInput:
    merged_item: Item = item | item.get("state", {})
    return ToeInput(
        state=ToeInputState(
            attacked_at=datetime.fromisoformat(merged_item["attacked_at"])
            if merged_item.get("attacked_at")
            else None,
            attacked_by=merged_item.get("attacked_by", ""),
            be_present=merged_item.get("be_present", True),
            be_present_until=datetime.fromisoformat(
                merged_item["be_present_until"]
            )
            if merged_item.get("be_present_until")
            else None,
            first_attack_at=datetime.fromisoformat(
                merged_item["first_attack_at"]
            )
            if merged_item.get("first_attack_at")
            else None,
            has_vulnerabilities=merged_item.get("has_vulnerabilities"),
            modified_by=merged_item.get("modified_by"),
            modified_date=datetime.fromisoformat(merged_item["modified_date"])
            if merged_item.get("modified_date")
            else None,
            seen_at=datetime.fromisoformat(merged_item["seen_at"])
            if merged_item.get("seen_at")
            else None,
            seen_first_time_by=merged_item["seen_first_time_by"],
            unreliable_root_id=merged_item.get("unreliable_root_id", ""),
        ),
        component=merged_item["component"],
        entry_point=merged_item["entry_point"],
        group_name=group_name,
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
        "component": toe_input.component,
        "entry_point": toe_input.entry_point,
        "group_name": toe_input.group_name,
        "state": {
            "attacked_at": ""
            if toe_input.state.attacked_at is None
            else db_model_utils.get_as_utc_iso_format(
                toe_input.state.attacked_at
            ),
            "attacked_by": toe_input.state.attacked_by,
            "be_present": toe_input.state.be_present,
            "be_present_until": ""
            if toe_input.state.be_present_until is None
            else db_model_utils.get_as_utc_iso_format(
                toe_input.state.be_present_until
            ),
            "first_attack_at": ""
            if toe_input.state.first_attack_at is None
            else db_model_utils.get_as_utc_iso_format(
                toe_input.state.first_attack_at
            ),
            "has_vulnerabilities": toe_input.state.has_vulnerabilities,
            "modified_by": toe_input.state.modified_by,
            "modified_date": get_as_utc_iso_format(
                toe_input.state.modified_date
            )
            if toe_input.state.modified_date
            else "",
            "seen_at": ""
            if toe_input.state.seen_at is None
            else db_model_utils.get_as_utc_iso_format(toe_input.state.seen_at),
            "seen_first_time_by": toe_input.state.seen_first_time_by,
            "unreliable_root_id": toe_input.state.unreliable_root_id,
        },
    }


def format_toe_input_metadata_item(
    state: ToeInputState, metadata: ToeInputMetadataToUpdate
) -> Item:
    metadata_item: Item = {}
    metadata_item["state"] = json.loads(json.dumps(state, default=serialize))
    if metadata.clean_attacked_at:
        metadata_item["attacked_at"] = ""
        metadata_item["state"]["attacked_at"] = ""
    if metadata.clean_be_present_until:
        metadata_item["be_present_until"] = ""
        metadata_item["state"]["be_present_until"] = ""
    if metadata.clean_first_attack_at:
        metadata_item["first_attack_at"] = ""
        metadata_item["state"]["first_attack_at"] = ""
    if metadata.clean_seen_at:
        metadata_item["seen_at"] = ""
        metadata_item["state"]["seen_at"] = ""

    return metadata_item
