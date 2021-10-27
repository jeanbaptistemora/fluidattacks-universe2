from .types import (
    ToeLines,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)


def format_toe_lines(item: Item) -> ToeLines:
    return ToeLines(
        attacked_at=item["attacked_at"],
        attacked_by=item["attacked_by"],
        attacked_lines=item["attacked_lines"],
        be_present=item["be_present"],
        comments=item["comments"],
        filename=item["filename"],
        first_attack_at=item["first_attack_at"],
        group_name=item["group_name"],
        loc=item["loc"],
        modified_commit=item["modified_commit"],
        modified_date=item["modified_date"],
        root_id=item["root_id"],
        seen_at=item["seen_at"],
        sorts_risk_level=item["sorts_risk_level"],
    )


def format_toe_lines_item(
    key: PrimaryKey, key_structure: PrimaryKey, toe_lines: ToeLines
) -> Item:
    return {
        key_structure.partition_key: key.partition_key,
        key_structure.sort_key: key.sort_key,
        "attacked_at": toe_lines.attacked_at,
        "attacked_by": toe_lines.attacked_by,
        "attacked_lines": toe_lines.attacked_lines,
        "be_present": toe_lines.be_present,
        "comments": toe_lines.comments,
        "filename": toe_lines.filename,
        "first_attack_at": toe_lines.first_attack_at,
        "group_name": toe_lines.group_name,
        "loc": toe_lines.loc,
        "modified_commit": toe_lines.modified_commit,
        "modified_date": toe_lines.modified_date,
        "root_id": toe_lines.root_id,
        "seen_at": toe_lines.seen_at,
        "sorts_risk_level": toe_lines.sorts_risk_level,
    }
