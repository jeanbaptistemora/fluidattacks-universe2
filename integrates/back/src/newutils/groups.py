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
    GroupMetadataToUpdate,
    GroupState,
    GroupStateRemovalJustification,
    GroupStateUpdationJustification,
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


def filter_active_groups(groups: tuple[Group, ...]) -> tuple[Group, ...]:
    return tuple(
        group
        for group in groups
        if group.state.status == GroupStateStatus.ACTIVE
    )


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


def format_group_state(
    state: Dict[str, Any],
    state_status: GroupStateStatus,
    pending_deletion_date: Optional[str],
    suscription_type: GroupSubscriptionType,
    tier: GroupTier,
) -> GroupState:
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
        status=state_status,
        tier=tier,
        type=suscription_type,
        comments=state.get("comments"),
        justification=format_state_justification(state.get("reason")),
        pending_deletion_date=convert_to_iso_str(pending_deletion_date)
        if pending_deletion_date
        else None,
        service=GroupService[str(state["service"]).upper()]
        if state.get("service")
        else None,
    )


def format_group(item: Item, organization_name: str) -> Group:
    state_status = (
        GroupStateStatus.ACTIVE
        if str(
            get_key_or_fallback(item, "group_status", "project_status")
        ).upper()
        == GroupStateStatus.ACTIVE.value
        else GroupStateStatus.DELETED
    )
    last_configuration: Dict[str, Any] = item["historic_configuration"][-1]
    suscription_type = GroupSubscriptionType[
        str(last_configuration["type"]).upper()
    ]
    tier = (
        GroupTier[str(last_configuration["tier"]).upper()]
        if last_configuration.get("tier")
        else GroupTier.OTHER
    )
    if (
        state_status == GroupStateStatus.DELETED
        and "historic_deletion" in item
    ):
        current_state: Dict[str, Any] = item["historic_deletion"][-1]
    else:
        current_state = last_configuration
    return Group(
        description=item.get("description", ""),
        language=GroupLanguage[item.get("language", "en").upper()],
        name=str(
            get_key_or_fallback(item, "group_name", "project_name")
        ).lower(),
        organization_name=organization_name,
        state=format_group_state(
            state=current_state,
            state_status=state_status,
            pending_deletion_date=item.get("pending_deletion_date"),
            suscription_type=suscription_type,
            tier=tier,
        ),
        agent_token=item.get("agent_token"),
        context=item.get("group_context"),
        disambiguation=item.get("disambiguation"),
        files=format_group_files(item["files"]) if item.get("files") else None,
        tags=set(item["tag"]) if item.get("tag") else None,
    )


def format_group_treatment_summary(
    treatment_data: Dict[str, int]
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
        closed_vulnerabilities=item.get("closed_vulnerabilities"),
        exposed_over_time_cvssf=item.get("exposed_over_time_cvssf"),
        exposed_over_time_month_cvssf=item.get(
            "exposed_over_time_month_cvssf"
        ),
        exposed_over_time_year_cvssf=item.get("exposed_over_time_year_cvssf"),
        last_closed_vulnerability_days=item.get("last_closing_date"),
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
        open_findings=item.get("open_findings"),
        open_vulnerabilities=item.get("open_vulnerabilities"),
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


def format_group_metadata_item(metadata: GroupMetadataToUpdate) -> Item:
    item = {
        "group_context": metadata.context,
    }
    return {
        key: None if not value else value
        for key, value in item.items()
        if value is not None
    }
