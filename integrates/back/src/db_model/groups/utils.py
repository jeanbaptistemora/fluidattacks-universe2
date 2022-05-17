from .constants import (
    ORGANIZATION_ID_PREFIX,
)
from .enums import (
    GroupLanguage,
    GroupService,
    GroupStateRemovalJustification,
    GroupStateStatus,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from .types import (
    Group,
    GroupFile,
    GroupState,
    GroupStatusJustification,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Any,
    Optional,
)


def add_org_id_prefix(organization_id: str) -> str:
    no_prefix_id = remove_org_id_prefix(organization_id)
    return f"{ORGANIZATION_ID_PREFIX}{no_prefix_id}"


def remove_org_id_prefix(organization_id: str) -> str:
    return organization_id.lstrip(ORGANIZATION_ID_PREFIX)


def serialize_sets(object_: Any) -> Any:
    if isinstance(object_, set):
        return list(object_)
    return object_


def format_files(files: list[dict[str, str]]) -> list[GroupFile]:
    return [
        GroupFile(
            description=file["description"],
            file_name=file["file_name"],
            modified_by=file["modified_by"],
            modified_date=file["modified_date"]
            if file.get("modified_date")
            else None,
        )
        for file in files
    ]


def format_group(item: Item) -> Group:
    return Group(
        agent_token=item.get("agent_token"),
        business_id=item.get("business_id"),
        business_name=item.get("business_name"),
        context=item.get("context"),
        description=item["description"],
        disambiguation=item.get("disambiguation"),
        files=format_files(item["files"]) if item.get("files") else None,
        language=GroupLanguage[item["language"]],
        name=item["name"],
        organization_id=add_org_id_prefix(item["organization_id"]),
        state=format_state(item["state"]),
        tags=set(item["tags"]) if item.get("tags") else None,
    )


def format_state(state: Item) -> GroupState:
    return GroupState(
        comments=state.get("comments"),
        has_machine=state["has_machine"],
        has_squad=state["has_squad"],
        managed=state.get("managed", True),
        justification=format_state_justification(state.get("justification")),
        modified_by=state["modified_by"],
        modified_date=state["modified_date"],
        pending_deletion_date=state.get("pending_deletion_date"),
        service=GroupService[state["service"]]
        if state.get("service")
        else None,
        status=GroupStateStatus[state["status"]],
        tier=GroupTier[state["tier"]]
        if state.get("tier")
        else GroupTier.OTHER,
        type=GroupSubscriptionType[state["type"]],
    )


def format_state_justification(
    justification: Optional[str],
) -> Optional[GroupStatusJustification]:
    if not justification:
        return None
    try:
        return GroupStateRemovalJustification[justification]
    except KeyError:
        pass
    try:
        return GroupStateUpdationJustification[justification]
    except KeyError:
        pass
    return None
