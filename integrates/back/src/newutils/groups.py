from datetime import (
    datetime,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupStateRemovalJustification,
    GroupStateStatus,
    GroupStateUpdationJustification,
    GroupSubscriptionType,
    GroupTier,
)
from db_model.groups.types import (
    Group,
    GroupFile,
    GroupMetadataToUpdate,
    GroupState,
    GroupStatusJustification,
    GroupTreatmentSummary,
    GroupUnreliableIndicators,
)
from dynamodb.types import (
    Item,
)
import logging
import logging.config
from newutils.datetime import (
    convert_from_iso_str,
    convert_to_iso_str,
    get_as_str,
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
    Optional,
    Union,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


def filter_active_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
    )


def format_group_files(files: list[dict[str, str]]) -> list[GroupFile]:
    return [
        GroupFile(
            description=file["description"],
            file_name=file["fileName"],
            modified_by=file["uploader"],
            modified_date=get_as_utc_iso_format(
                get_from_str(
                    date_str=file["uploadDate"],
                    date_format="%Y-%m-%d %H:%M",
                )
            )
            if "uploadDate" in file
            else None,
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


def format_group_state(state: Item) -> GroupState:
    justification: (
        Union[
            GroupStateUpdationJustification, Optional[GroupStatusJustification]
        ]
    )
    has_machine: bool = bool(
        get_key_or_fallback(state, "has_machine", "has_skims", False)
    )
    has_squad: bool = bool(
        get_key_or_fallback(state, "has_squad", "has_drills", False)
    )
    if state.get("reason") and "with event" in state["reason"]:
        comments: Optional[str] = state["reason"]
        justification = GroupStateUpdationJustification.OTHER
    else:
        comments = state.get("comments")
        justification = format_state_justification(state.get("reason"))

    return GroupState(
        comments=comments,
        has_machine=has_machine,
        has_squad=has_squad,
        justification=justification,
        modified_by=str(state.get("requester")) or str(state.get("user")),
        modified_date=convert_to_iso_str(state["date"]),
        service=GroupService[str(state["service"]).upper()]
        if state.get("service")
        else None,
        status=GroupStateStatus.ACTIVE,
        tier=GroupTier[str(state["tier"]).upper()]
        if state.get("tier")
        else GroupTier.OTHER,
        type=GroupSubscriptionType[str(state["type"]).upper()],
    )


def format_group_historic_state(item: Item) -> tuple[GroupState, ...]:
    historic_configuration: list[Item] = item["historic_configuration"]
    historic_state = [
        format_group_state(entry) for entry in historic_configuration
    ]

    state_status = (
        GroupStateStatus.ACTIVE
        if str(
            get_key_or_fallback(item, "group_status", "project_status")
        ).upper()
        == GroupStateStatus.ACTIVE.value
        else GroupStateStatus.DELETED
    )
    if state_status == GroupStateStatus.DELETED:
        if item.get("historic_deletion"):
            last_state: GroupState = historic_state[-1]
            last_deletion_state: dict[str, str] = item["historic_deletion"][-1]
            deletion_requester = last_deletion_state["user"]
            deletion_date = last_deletion_state["date"]
            historic_state.append(
                last_state._replace(
                    modified_by=deletion_requester,
                    modified_date=convert_to_iso_str(deletion_date),
                )
            )
        historic_state = [
            *historic_state[:-1],
            historic_state[-1]._replace(
                status=GroupStateStatus.DELETED,
            ),
        ]
    elif item.get("pending_deletion_date"):
        historic_state = [
            *historic_state[:-1],
            historic_state[-1]._replace(
                pending_deletion_date=convert_to_iso_str(
                    item["pending_deletion_date"]
                )
            ),
        ]

    return tuple(historic_state)


def format_group(item: Item, organization_name: str) -> Group:
    historic_state = format_group_historic_state(item)
    return Group(
        business_id=item.get("business_id", None),
        business_name=item.get("business_name", None),
        description=item.get("description", ""),
        language=GroupLanguage[item.get("language", "en").upper()],
        name=str(
            get_key_or_fallback(item, "group_name", "project_name")
        ).lower(),
        organization_name=organization_name,
        state=historic_state[-1],
        agent_token=item.get("agent_token"),
        context=item.get("group_context"),
        disambiguation=item.get("disambiguation"),
        files=format_group_files(item["files"]) if item.get("files") else None,
        tags=set(item["tag"]) if item.get("tag") else None,
    )


def format_group_treatment_summary(
    treatment_data: dict[str, int]
) -> GroupTreatmentSummary:
    return GroupTreatmentSummary(
        accepted=int(treatment_data.get("accepted", 0)),
        accepted_undefined=int(treatment_data.get("acceptedUndefined", 0)),
        in_progress=int(treatment_data.get("inProgress", 0)),
        new=int(treatment_data.get("undefined", 0)),
    )


def format_group_unreliable_indicators(
    item: Item,
) -> GroupUnreliableIndicators:
    return GroupUnreliableIndicators(
        closed_vulnerabilities=int(item["closed_vulnerabilities"])
        if "closed_vulnerabilities" in item
        else None,
        exposed_over_time_cvssf=item.get("exposed_over_time_cvssf"),
        exposed_over_time_month_cvssf=item.get(
            "exposed_over_time_month_cvssf"
        ),
        exposed_over_time_year_cvssf=item.get("exposed_over_time_year_cvssf"),
        last_closed_vulnerability_days=int(item["last_closing_date"])
        if "last_closing_date" in item
        else None,
        last_closed_vulnerability_finding=item.get(
            "last_closing_vuln_finding"
        ),
        max_open_severity=item.get("max_open_severity"),
        max_open_severity_finding=item.get("max_open_severity_finding"),
        mean_remediate=item.get("mean_remediate"),
        mean_remediate_critical_severity=item.get(
            "mean_remediate_critical_severity"
        ),
        mean_remediate_high_severity=item.get("mean_remediate_high_severity"),
        mean_remediate_low_severity=item.get("mean_remediate_low_severity"),
        mean_remediate_medium_severity=item.get(
            "mean_remediate_medium_severity"
        ),
        open_findings=int(item["open_findings"])
        if "open_findings" in item
        else None,
        open_vulnerabilities=int(item["open_vulnerabilities"])
        if "open_vulnerabilities" in item
        else None,
        remediated_over_time=item.get("remediated_over_time"),
        remediated_over_time_30=item.get("remediated_over_time_30"),
        remediated_over_time_90=item.get("remediated_over_time_90"),
        remediated_over_time_cvssf=item.get("remediated_over_time_cvssf"),
        remediated_over_time_cvssf_30=item.get(
            "remediated_over_time_cvssf_30"
        ),
        remediated_over_time_cvssf_90=item.get(
            "remediated_over_time_cvssf_90"
        ),
        remediated_over_time_month=item.get("remediated_over_time_month"),
        remediated_over_time_month_cvssf=item.get(
            "remediated_over_time_month_cvssf"
        ),
        remediated_over_time_year=item.get("remediated_over_time_year"),
        remediated_over_time_year_cvssf=item.get(
            "remediated_over_time_year_cvssf"
        ),
        treatment_summary=format_group_treatment_summary(
            item["total_treatment"]
        )
        if item.get("total_treatment")
        else None,
    )


def format_group_files_item(
    group_files: list[GroupFile],
) -> list[Item]:
    return [
        {
            "description": file.description,
            "fileName": file.file_name,
            "uploader": file.modified_by,
            "uploadDate": get_as_str(
                date=datetime.fromisoformat(file.modified_date),
                date_format="%Y-%m-%d %H:%M",
            )
            if file.modified_date
            else None,
        }
        for file in group_files
    ]


def format_group_metadata_item(metadata: GroupMetadataToUpdate) -> Item:
    item = {
        "agent_token": metadata.agent_token,
        "business_id": metadata.business_id,
        "business_name": metadata.business_name,
        "description": metadata.description,
        "disambiguation": metadata.disambiguation,
        "group_context": metadata.context,
        "files": format_group_files_item(metadata.files)
        if metadata.files is not None
        else None,
        "language": str(metadata.language.value).lower()
        if metadata.language
        else None,
        "tag": metadata.tags,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }


def format_group_state_item(state: GroupState) -> Item:
    item = {
        "comments": state.comments,
        "date": convert_from_iso_str(state.modified_date),
        "has_skims": state.has_machine,
        "has_machine": state.has_machine,
        "has_drills": state.has_squad,
        "has_squad": state.has_squad,
        "has_forces": True,
        "reason": state.justification.value if state.justification else None,
        "requester": state.modified_by,
        "service": state.service.value if state.service else None,
        "tier": str(state.tier.value).lower(),
        "type": str(state.type.value).lower(),
    }
    return {
        key: None if not value and value is not False else value
        for key, value in item.items()
        if value is not None
    }


def format_group_to_add_item(group: Group) -> Item:
    return {
        "project_name": group.name,
        "group_name": group.name,
        "description": group.description,
        "language": str(group.language.value).lower(),
        "historic_configuration": [
            {
                "date": convert_from_iso_str(group.state.modified_date),
                "has_skims": group.state.has_machine,
                "has_drills": group.state.has_squad,
                "has_forces": True,
                "requester": group.state.modified_by,
                "service": (
                    group.state.service.value if group.state.service else None
                ),
                "tier": str(group.state.tier.value).lower(),
                "type": str(group.state.type.value).lower(),
            }
        ],
        "project_status": group.state.status,
        "group_status": group.state.status,
    }
