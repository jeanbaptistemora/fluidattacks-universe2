from .types import (
    ToePort,
    ToePortEdge,
    ToePortState,
)
from datetime import (
    datetime,
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


def format_state(item: Item) -> ToePortState:
    return ToePortState(
        attacked_at=datetime.fromisoformat(item["attacked_at"])
        if item.get("attacked_at")
        else None,
        attacked_by=item.get("attacked_by"),
        be_present=item["be_present"],
        be_present_until=datetime.fromisoformat(item["be_present_until"])
        if item.get("be_present_until")
        else None,
        first_attack_at=datetime.fromisoformat(item["first_attack_at"])
        if item.get("first_attack_at")
        else None,
        has_vulnerabilities=item["has_vulnerabilities"],
        modified_by=item.get("modified_by"),
        modified_date=datetime.fromisoformat(item["modified_date"])
        if "modified_date" in item
        else None,
    )


def format_state_item(state: ToePortState) -> Item:
    return {
        "attacked_at": None
        if state.attacked_at is None
        else db_model_utils.get_as_utc_iso_format(state.attacked_at),
        "attacked_by": state.attacked_by,
        "be_present": state.be_present,
        "be_present_until": None
        if state.be_present_until is None
        else db_model_utils.get_as_utc_iso_format(state.be_present_until),
        "first_attack_at": None
        if state.first_attack_at is None
        else db_model_utils.get_as_utc_iso_format(state.first_attack_at),
        "has_vulnerabilities": state.has_vulnerabilities,
        "modified_by": state.modified_by,
        "modified_date": db_model_utils.get_as_utc_iso_format(
            state.modified_date
        )
        if state.modified_date
        else None,
    }


def format_toe_port(
    item: Item,
) -> ToePort:
    return ToePort(
        group_name=item["group_name"],
        address=item["address"],
        port=item["port"],
        root_id=item["root_id"],
        seen_at=datetime.fromisoformat(item["seen_at"])
        if item.get("seen_at")
        else None,
        seen_first_time_by=item.get("seen_first_time_by"),
        state=format_state(item["state"]),
    )


def format_toe_port_edge(
    index: Index | None,
    item: Item,
    table: Table,
) -> ToePortEdge:
    return ToePortEdge(
        node=format_toe_port(item),
        cursor=get_cursor(index, item, table),
    )


def format_toe_port_item(
    primary_key: PrimaryKey,
    key_structure: PrimaryKey,
    gsi_2_key: PrimaryKey,
    gsi_2_index: Index,
    toe_port: ToePort,
) -> Item:
    return {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        "address": toe_port.address,
        "group_name": toe_port.group_name,
        "port": toe_port.port,
        "root_id": toe_port.root_id,
        "seen_at": None
        if toe_port.seen_at is None
        else db_model_utils.get_as_utc_iso_format(toe_port.seen_at),
        "seen_first_time_by": toe_port.seen_first_time_by,
        "state": format_state_item(toe_port.state),
    }
