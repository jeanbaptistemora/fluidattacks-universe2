from .types import (
    SortsSuggestion,
    ToeLines,
    ToeLinesEdge,
    ToeLinesState,
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
from typing import (
    Optional,
)


def format_toe_lines_sorts_suggestions(
    suggestions: list[Item],
) -> list[SortsSuggestion]:
    return [
        SortsSuggestion(
            finding_title=suggestion["finding_title"],
            probability=int(suggestion["probability"]),
        )
        for suggestion in suggestions
    ]


def format_toe_lines(item: Item) -> ToeLines:
    state_modified_date = item.get("state", {}).get("modified_date")
    return ToeLines(
        filename=item["filename"],
        group_name=item["group_name"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        root_id=item["root_id"],
        seen_first_time_by=item.get("seen_first_time_by"),
        state=ToeLinesState(
            attacked_at=datetime.fromisoformat(item["attacked_at"])
            if item.get("attacked_at")
            else None,
            attacked_by=item["attacked_by"],
            attacked_lines=int(item["attacked_lines"]),
            be_present=item["be_present"],
            be_present_until=datetime.fromisoformat(item["be_present_until"])
            if item.get("be_present_until")
            else None,
            comments=item["comments"],
            first_attack_at=datetime.fromisoformat(item["first_attack_at"])
            if item.get("first_attack_at")
            else None,
            has_vulnerabilities=item.get("has_vulnerabilities"),
            last_author=item["last_author"],
            last_commit=item["last_commit"],
            loc=int(item["loc"]),
            modified_by=item.get("state", {}).get("modified_by"),
            modified_date=datetime.fromisoformat(state_modified_date)
            if state_modified_date
            else None,
            seen_at=datetime.fromisoformat(item["seen_at"]),
            sorts_risk_level=int(item["sorts_risk_level"]),
            sorts_risk_level_date=datetime.fromisoformat(
                item["sorts_risk_level_date"]
            )
            if item.get("sorts_risk_level_date")
            else None,
            sorts_suggestions=format_toe_lines_sorts_suggestions(
                item["sorts_suggestions"]
            )
            if item.get("sorts_suggestions")
            else None,
        ),
    )


def format_toe_lines_edge(
    index: Optional[Index],
    item: Item,
    table: Table,
) -> ToeLinesEdge:
    return ToeLinesEdge(
        node=format_toe_lines(item), cursor=get_cursor(index, item, table)
    )


def format_toe_lines_sorts_suggestions_item(
    suggestions: list[SortsSuggestion],
) -> list[Item]:
    return [
        {
            "finding_title": suggestion.finding_title,
            "probability": suggestion.probability,
        }
        for suggestion in suggestions
    ]


def format_toe_lines_item(
    primary_key: PrimaryKey,
    key_structure: PrimaryKey,
    gsi_2_key: PrimaryKey,
    gsi_2_index: Index,
    toe_lines: ToeLines,
) -> Item:
    return {
        key_structure.partition_key: primary_key.partition_key,
        key_structure.sort_key: primary_key.sort_key,
        gsi_2_index.primary_key.sort_key: gsi_2_key.sort_key,
        gsi_2_index.primary_key.partition_key: gsi_2_key.partition_key,
        "attacked_at": get_as_utc_iso_format(toe_lines.state.attacked_at)
        if toe_lines.state.attacked_at
        else None,
        "attacked_by": toe_lines.state.attacked_by,
        "attacked_lines": toe_lines.state.attacked_lines,
        "be_present": toe_lines.state.be_present,
        "be_present_until": get_as_utc_iso_format(
            toe_lines.state.be_present_until
        )
        if toe_lines.state.be_present_until
        else None,
        "comments": toe_lines.state.comments,
        "filename": toe_lines.filename,
        "first_attack_at": get_as_utc_iso_format(
            toe_lines.state.first_attack_at
        )
        if toe_lines.state.first_attack_at
        else None,
        "group_name": toe_lines.group_name,
        "has_vulnerabilities": toe_lines.state.has_vulnerabilities,
        "last_author": toe_lines.state.last_author,
        "last_commit": toe_lines.state.last_commit,
        "loc": toe_lines.state.loc,
        "modified_date": get_as_utc_iso_format(toe_lines.modified_date),
        "root_id": toe_lines.root_id,
        "seen_at": get_as_utc_iso_format(toe_lines.state.seen_at),
        "seen_first_time_by": toe_lines.seen_first_time_by,
        "sorts_risk_level": toe_lines.state.sorts_risk_level,
        "sorts_risk_level_date": get_as_utc_iso_format(
            toe_lines.state.sorts_risk_level_date
        )
        if toe_lines.state.sorts_risk_level_date
        else None,
        "sorts_suggestions": format_toe_lines_sorts_suggestions_item(
            toe_lines.state.sorts_suggestions
        )
        if toe_lines.state.sorts_suggestions
        else None,
        "state": {
            "modified_by": toe_lines.state.modified_by,
            "modified_date": get_as_utc_iso_format(
                toe_lines.state.modified_date
            )
            if toe_lines.state.modified_date
            else None,
        },
    }
