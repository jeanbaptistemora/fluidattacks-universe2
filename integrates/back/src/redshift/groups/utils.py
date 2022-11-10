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

FLUID_IDENTIFIER = "@fluidattacks.com"


def format_row_code_languages(
    group_name: str,
    item: Item,
) -> list[Item]:
    unreliable_code_languages = item.get("code_languages", [])
    return [
        dict(
            id=hashlib.sha256(
                (group_name + language_item["language"]).encode("utf-8")
            ).hexdigest(),
            group_name=group_name,
            language=language_item["language"],
            loc=int(language_item["loc"]),
        )
        for language_item in unreliable_code_languages
    ]


def format_row_metadata(
    item: Item,
) -> Item:
    return dict(
        id=item["name"],
        created_by=item["created_by"]
        if str(item["created_by"]).endswith(FLUID_IDENTIFIER)
        else None,
        created_date=item["created_date"],
        language=item["language"],
        name=item["name"],
        organization_id=item["organization_id"],
        sprint_duration=int(item["sprint_duration"])
        if item.get("sprint_duration")
        else None,
        sprint_start_date=datetime.fromisoformat(item["sprint_start_date"])
        if item.get("sprint_start_date")
        else None,
    )


def format_row_state(
    group_name: str,
    state: Item,
) -> Item:
    return dict(
        id=group_name,
        has_machine=bool(state["has_machine"]),
        has_squad=bool(state["has_squad"]),
        justification=state.get("justification"),
        managed=state["managed"] if state.get("managed") else "NOT_MANAGED",
        modified_by=state["modified_by"]
        if str(state["modified_by"]).endswith(FLUID_IDENTIFIER)
        else None,
        modified_date=datetime.fromisoformat(state["modified_date"]),
        pending_deletion_date=datetime.fromisoformat(
            state["pending_deletion_date"]
        )
        if state.get("pending_deletion_date")
        else None,
        service=state.get("service"),
        status=state["status"],
        tier=state["tier"] if state.get("tier") else "OTHER",
        type=state["type"],
    )
