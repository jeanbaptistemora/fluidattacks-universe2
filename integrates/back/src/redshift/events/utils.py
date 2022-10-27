# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
)

FLUID_IDENTIFIER = "@fluidattacks.com"


def format_row_metadata(
    item: Item,
) -> Item:
    unreliable_solving_date: Optional[str] = item.get(
        "unreliable_indicators", {}
    ).get("unreliable_solving_date", None)
    return dict(
        id=item["id"],
        created_by=item["created_by"]
        if str(item["created_by"]).endswith(FLUID_IDENTIFIER)
        else None,
        created_date=datetime.fromisoformat(item["created_date"])
        if item.get("created_date")
        else None,
        event_date=datetime.fromisoformat(item["event_date"])
        if item.get("event_date")
        else None,
        group_name=item["group_name"],
        hacker=item["hacker"],
        root_id=item.get("root_id"),
        solving_date=datetime.fromisoformat(unreliable_solving_date)
        if unreliable_solving_date
        else None,
        status=item["state"]["status"],
        type=item["type"],
    )
