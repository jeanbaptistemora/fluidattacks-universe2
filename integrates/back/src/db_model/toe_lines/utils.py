from .types import (
    ToeLines,
    ToeLinesEdge,
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


def format_toe_lines(item: Item) -> ToeLines:
    return ToeLines(
        attacked_at=item["attacked_at"],
        attacked_by=item["attacked_by"],
        attacked_lines=int(item["attacked_lines"]),
        be_present=item["be_present"],
        be_present_until=item["be_present_until"],
        comments=item["comments"],
        commit_author=item["commit_author"],
        filename=item["filename"],
        first_attack_at=item["first_attack_at"],
        group_name=item["group_name"],
        is_deactivated=item["is_deactivated"],
        loc=int(item["loc"]),
        modified_commit=item["modified_commit"],
        modified_date=item["modified_date"],
        root_id=item["root_id"],
        seen_at=item["seen_at"],
        sorts_risk_level=int(item["sorts_risk_level"]),
    )


def format_toe_lines_edge(
    index: Optional[Index],
    item: Item,
    table: Table,
) -> ToeLinesEdge:
    return ToeLinesEdge(
        node=format_toe_lines(item), cursor=get_cursor(index, item, table)
    )


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
        "attacked_at": toe_lines.attacked_at,
        "attacked_by": toe_lines.attacked_by,
        "attacked_lines": toe_lines.attacked_lines,
        "be_present": toe_lines.be_present,
        "be_present_until": toe_lines.be_present_until,
        "comments": toe_lines.comments,
        "commit_author": toe_lines.commit_author,
        "filename": toe_lines.filename,
        "first_attack_at": toe_lines.first_attack_at,
        "group_name": toe_lines.group_name,
        "is_deactivated": toe_lines.is_deactivated,
        "loc": toe_lines.loc,
        "modified_commit": toe_lines.modified_commit,
        "modified_date": toe_lines.modified_date,
        "root_id": toe_lines.root_id,
        "seen_at": toe_lines.seen_at,
        "sorts_risk_level": toe_lines.sorts_risk_level,
    }
