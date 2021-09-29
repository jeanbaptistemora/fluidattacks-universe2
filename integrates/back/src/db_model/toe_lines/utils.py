from .types import (
    ToeLines,
)
from dynamodb.types import (
    Item,
    PrimaryKey,
)


def format_toe_lines(
    *,
    group_name: str,
    key_structure: PrimaryKey,
    item: Item,
) -> ToeLines:
    sort_key_items = item[key_structure.sort_key].split("#", 4)
    root_id = sort_key_items[2]
    filename = sort_key_items[4]
    return ToeLines(
        comments=item["comments"],
        filename=filename,
        group_name=group_name,
        loc=item["loc"],
        modified_commit=item["modified_commit"],
        modified_date=item["modified_date"],
        root_id=root_id,
        tested_date=item["tested_date"],
        tested_lines=item["tested_lines"],
        sorts_risk_level=item["sorts_risk_level"],
    )
