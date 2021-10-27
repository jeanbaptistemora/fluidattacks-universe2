from .types import (
    ToeLines,
)
from dynamodb.types import (
    Item,
)


def format_toe_lines(
    *,
    item: Item,
) -> ToeLines:
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
