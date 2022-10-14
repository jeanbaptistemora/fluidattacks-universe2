# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=hash(
            (
                item["unreliable_root_id"],
                item["component"],
                item["entry_point"],
            )
        ),
        attacked_at=datetime.fromisoformat(item["attacked_at"])
        if item.get("attacked_at")
        else None,
        attacked_by=item["attacked_by"],
        be_present=bool(item["be_present"]),
        be_present_until=datetime.fromisoformat(item["be_present_until"])
        if item.get("be_present_until")
        else None,
        first_attack_at=datetime.fromisoformat(item["first_attack_at"])
        if item.get("first_attack_at")
        else None,
        group_name=item["group_name"],
        has_vulnerabilities=bool(item.get("has_vulnerabilities", False)),
        root_id=item["unreliable_root_id"],
        seen_at=datetime.fromisoformat(item["seen_at"])
        if item.get("seen_at")
        else None,
        seen_first_time_by=item["seen_first_time_by"],
    )
