# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)

FLUID_IDENTIFIER = "@fluidattacks.com"
ORGANIZATION_ID_PREFIX = "ORG#"


def _remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=_remove_org_id_prefix(item["id"]),
        country=item.get("country"),
        created_by=item["created_by"]
        if str(item.get("created_by", "")).endswith(FLUID_IDENTIFIER)
        else None,
        created_date=datetime.fromisoformat(item["created_date"])
        if item.get("created_date")
        else None,
        name=item["name"],
    )


def format_row_state(
    state: Item,
    organization_id: str,
) -> Item:
    return dict(
        id=_remove_org_id_prefix(organization_id),
        modified_by=state["modified_by"]
        if str(state["modified_by"]).endswith(FLUID_IDENTIFIER)
        else None,
        modified_date=datetime.fromisoformat(state["modified_date"]),
        pending_deletion_date=datetime.fromisoformat(
            state["pending_deletion_date"]
        )
        if state.get("pending_deletion_date")
        else None,
        status=state["status"],
    )
