from datetime import (
    datetime,
)
from dynamodb.types import (
    Item,
)
import hashlib

FLUID_IDENTIFIER = "@fluidattacks.com"


def format_row_code_languages(
    unreliable_indicators: Item,
) -> list[Item]:
    group_name = str(unreliable_indicators["pk"]).split("#")[1]
    unreliable_code_languages = unreliable_indicators.get("code_languages", [])
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
        if str(item.get("created_by", "")).endswith(FLUID_IDENTIFIER)
        else None,
        created_date=datetime.fromisoformat(item["created_date"])
        if item.get("created_date")
        else None,
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


def _format_state_managed(managed: bool | str) -> str:
    if not managed:
        return "NOT_MANAGED"
    if managed is True:
        return "MANAGED"
    return str(managed)


def format_row_state(
    group_name: str,
    state: Item,
) -> Item:
    return dict(
        id=group_name,
        comments=state.get("comments"),
        has_machine=bool(state["has_machine"]),
        has_squad=bool(state["has_squad"]),
        justification=state.get("justification"),
        managed=_format_state_managed(state.get("managed", "")),
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
