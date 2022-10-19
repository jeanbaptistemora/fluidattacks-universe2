# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
import hashlib


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=hashlib.sha256(item["sk"].encode("utf-8")).hexdigest(),
        attacked_at=datetime.fromisoformat(item["attacked_at"])
        if item.get("attacked_at")
        else None,
        attacked_by=item["attacked_by"],
        attacked_lines=int(item["attacked_lines"]),
        be_present=bool(item["be_present"]),
        be_present_until=datetime.fromisoformat(item["be_present_until"])
        if item.get("be_present_until")
        else None,
        first_attack_at=datetime.fromisoformat(item["first_attack_at"])
        if item.get("first_attack_at")
        else None,
        group_name=item["group_name"],
        has_vulnerabilities=bool(item.get("has_vulnerabilities", False)),
        loc=item["loc"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        root_id=item["root_id"],
        seen_at=datetime.fromisoformat(item["seen_at"]),
        seen_first_time_by=item.get("seen_first_time_by"),
        sorts_risk_level=int(item["sorts_risk_level"]),
    )
