from custom_types import (
    Group as GroupType,
    Historic as HistoricType,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupStateStatus,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupState,
    GroupStateRemovalJustification,
    GroupStateUpdationJustification,
    GroupStatusJustification,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils.datetime import (
    convert_to_iso_str,
    get_as_utc_iso_format,
    get_from_str,
)
from newutils.utils import (
    get_key_or_fallback,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    Dict,
    List,
    Optional,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def has_asm_services(group: GroupType) -> bool:
    historic_configuration: HistoricType = group.get(
        "historic_configuration", [{}]
    )
    last_config_info = historic_configuration[-1]
    group_has_asm_services: bool = (
        get_key_or_fallback(last_config_info, "has_squad", "has_drills")
        or last_config_info["has_forces"]
    )

    return group_has_asm_services


def format_group_files(files: List[Dict[str, str]]) -> List[GroupFile]:
    return [
        GroupFile(
            description=file["description"],
            filename=file["fileName"],
            modified_by=file["uploader"],
            modified_date=get_as_utc_iso_format(
                get_from_str(
                    date_str=file["uploadDate"],
                    date_format="%Y-%m-%d %H:%M",
                )
            ),
        )
        for file in files
    ]


def format_state_justification(
    justification: Optional[str],
) -> Optional[GroupStatusJustification]:
    if not justification:
        return None
    justification = justification.upper()
    try:
        return GroupStateRemovalJustification[justification]
    except KeyError:
        pass
    try:
        return GroupStateUpdationJustification[justification]
    except KeyError:
        pass
    return None


def format_group_state(state: Dict[str, Any], state_status: str) -> GroupState:
    has_machine: bool = get_key_or_fallback(
        state, "has_machine", "has_skims", False
    )
    has_squad: bool = get_key_or_fallback(
        state, "has_squad", "has_drills", False
    )
    return GroupState(
        has_machine=has_machine,
        has_squad=has_squad,
        modified_by=state.get("requester") or state.get("user"),
        modified_date=convert_to_iso_str(state["date"]),
        service=GroupService[str(state["service"]).upper()],
        status=GroupStateStatus.ACTIVE
        if state_status.upper() == GroupStateStatus.ACTIVE.value
        else GroupStateStatus.DELETED,
        tier=GroupTier[str(state["tier"]).upper()],
        type=GroupSubscriptionType[str(state["type"]).upper()],
        comments=state.get("comments"),
        justification=format_state_justification(state.get("reason")),
    )


def format_group(item: Item, organization_name: str) -> Group:
    if "historic_deletion" in item:
        current_configuration: Dict[str, Any] = item["historic_deletion"][-1]
    else:
        current_configuration = item["historic_configuration"][-1]
    return Group(
        description=item.get("description", ""),
        language=GroupLanguage[item.get("language", "en").upper()],
        name=str(item["project_name"]).lower(),
        organization_name=organization_name,
        state=format_group_state(
            state=current_configuration,
            state_status=item["project_status"],
        ),
        agent_token=item.get("agent_token"),
        context=item.get("group_context"),
        disambiguation=item.get("disambiguation"),
        files=format_group_files(item["files"]) if item.get("files") else None,
        tags=set(item["tag"]) if item.get("tag") else None,
    )
