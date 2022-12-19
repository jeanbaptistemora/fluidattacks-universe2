from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityToolImpact,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from .types import (
    Vulnerability,
    VulnerabilityEdge,
    VulnerabilityHistoricEntry,
    VulnerabilityState,
    VulnerabilityTool,
    VulnerabilityTreatment,
    VulnerabilityUnreliableIndicators,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from custom_exceptions import (
    VulnerabilityEntryNotFound,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.vulnerabilities.constants import (
    ZR_FILTER_STATUSES,
    ZR_INDEX_METADATA,
)
from dynamodb import (
    keys,
)
from dynamodb.types import (
    Index,
    Item,
    PrimaryKey,
    Table,
)
from dynamodb.utils import (
    get_cursor,
)
from serializers import (
    Snippet,
)
from typing import (
    Any,
    Optional,
)


def filter_non_deleted(
    vulnerabilities: tuple[Vulnerability, ...],
) -> tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.state.status
        not in {
            VulnerabilityStateStatus.DELETED,
            VulnerabilityStateStatus.MASKED,
        }
    )


def filter_non_zero_risk(
    vulnerabilities: tuple[Vulnerability, ...],
) -> tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if not vuln.zero_risk
        or vuln.zero_risk.status
        not in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
    )


def filter_non_zero_risk_confirmed(
    vulnerabilities: tuple[Vulnerability, ...],
) -> tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if not vuln.zero_risk
        or vuln.zero_risk.status not in VulnerabilityZeroRiskStatus.CONFIRMED
    )


def filter_zero_risk(
    vulnerabilities: tuple[Vulnerability, ...],
) -> tuple[Vulnerability, ...]:
    return tuple(
        vuln
        for vuln in vulnerabilities
        if vuln.zero_risk
        and vuln.zero_risk.status
        in (
            VulnerabilityZeroRiskStatus.CONFIRMED,
            VulnerabilityZeroRiskStatus.REQUESTED,
        )
    )


def format_vulnerability(item: Item) -> Vulnerability:
    state = format_state(item["state"])
    treatment = (
        format_treatment(item["treatment"]) if "treatment" in item else None
    )
    verification = (
        format_verification(item["verification"])
        if "verification" in item
        else None
    )
    zero_risk = (
        format_zero_risk(item["zero_risk"]) if "zero_risk" in item else None
    )
    unreliable_indicators = (
        format_unreliable_indicators(item["unreliable_indicators"])
        if "unreliable_indicators" in item
        else VulnerabilityUnreliableIndicators()
    )

    return Vulnerability(
        bug_tracking_system_url=item.get("bug_tracking_system_url", None),
        created_by=item["created_by"],
        created_date=datetime.fromisoformat(item["created_date"]),
        custom_severity=(
            int(item["custom_severity"])
            if "custom_severity" in item
            and item["custom_severity"] is not None
            and item["custom_severity"]
            else None
        ),
        developer=item.get("developer", None),
        event_id=item.get("pk_4", None),
        finding_id=item["sk"].split("#")[1],
        group_name=item["group_name"],
        hacker_email=item["hacker_email"],
        hash=item.get("hash", None),
        id=item["pk"].split("#")[1],
        root_id=item.get("root_id", None),
        skims_method=item.get("skims_method", None),
        skims_technique=item.get("skims_technique", None),
        state=state,
        stream=item.get("stream", None),
        tags=item.get("tags", None),
        treatment=treatment,
        type=VulnerabilityType[item["type"]],
        unreliable_indicators=unreliable_indicators,
        verification=verification,
        zero_risk=zero_risk,
    )


def format_vulnerability_edge(
    index: Optional[Index],
    item: Item,
    table: Table,
) -> VulnerabilityEdge:
    return VulnerabilityEdge(
        node=format_vulnerability(item), cursor=get_cursor(index, item, table)
    )


def _format_snippet(
    snippet: Optional[dict[str, Any]] = None
) -> Optional[Snippet]:
    if not snippet or isinstance(snippet, str):
        return None
    return Snippet(
        content=snippet["content"],
        offset=snippet["offset"],
        line=snippet["line"],
        column=snippet.get("column"),
        columns_per_line=snippet["columns_per_line"],
        line_context=snippet["line_context"],
        highlight_line_number=snippet["highlight_line_number"],
        show_line_numbers=snippet["show_line_numbers"],
        wrap=snippet["wrap"],
    )


def format_state(item: Item) -> VulnerabilityState:
    tool = format_tool(item["tool"]) if "tool" in item else None
    return VulnerabilityState(
        commit=item.get("commit"),
        justification=StateRemovalJustification[item["justification"]]
        if item.get("justification", None)
        else None,
        modified_by=item["modified_by"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        source=Source[item["source"]],
        specific=item["specific"],
        status=VulnerabilityStateStatus[item["status"]],
        tool=tool,
        where=item["where"],
        snippet=_format_snippet(item.get("snippet")),
    )


def format_tool(item: Item) -> VulnerabilityTool:
    return VulnerabilityTool(
        name=item["name"], impact=VulnerabilityToolImpact[item["impact"]]
    )


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=datetime.fromisoformat(item["accepted_until"])
        if item.get("accepted_until")
        else None,
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if item.get("acceptance_status", None)
        else None,
        justification=item.get("justification", None),
        assigned=item.get("assigned", None),
        modified_by=item.get("modified_by", None),
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityTreatmentStatus[item["status"]],
    )


def format_unreliable_indicators(
    item: Item,
) -> VulnerabilityUnreliableIndicators:
    return VulnerabilityUnreliableIndicators(
        unreliable_closing_date=item.get("unreliable_closing_date", None),
        unreliable_efficacy=item.get("unreliable_efficacy", None),
        unreliable_last_reattack_date=item.get(
            "unreliable_last_reattack_date", None
        ),
        unreliable_last_reattack_requester=item.get(
            "unreliable_last_reattack_requester", None
        ),
        unreliable_last_requested_reattack_date=item.get(
            "unreliable_last_requested_reattack_date", None
        ),
        unreliable_reattack_cycles=None
        if item.get("unreliable_reattack_cycles", None) is None
        else int(item["unreliable_reattack_cycles"]),
        unreliable_source=Source[item["unreliable_source"]],
        unreliable_treatment_changes=None
        if item.get("unreliable_treatment_changes", None) is None
        else int(item["unreliable_treatment_changes"]),
    )


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        event_id=item.get("event_id", None),
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_zero_risk(item: Item) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=item["comment_id"],
        modified_by=item["modified_by"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        status=VulnerabilityZeroRiskStatus[item["status"]],
    )


def historic_entry_type_to_str(item: VulnerabilityHistoricEntry) -> str:
    if isinstance(item, VulnerabilityState):
        return "state"
    if isinstance(item, VulnerabilityTreatment):
        return "treatment"
    if isinstance(item, VulnerabilityVerification):
        return "verification"
    if isinstance(item, VulnerabilityZeroRisk):
        return "zero_risk"
    return ""


def get_current_entry(
    entry: VulnerabilityHistoricEntry, current_value: Vulnerability
) -> Optional[VulnerabilityHistoricEntry]:
    if isinstance(entry, VulnerabilityState):
        return current_value.state
    if isinstance(entry, VulnerabilityTreatment):
        return current_value.treatment
    if isinstance(entry, VulnerabilityVerification):
        return current_value.verification
    if isinstance(entry, VulnerabilityZeroRisk):
        return current_value.zero_risk

    raise VulnerabilityEntryNotFound()


def get_assigned(*, treatment: Optional[VulnerabilityTreatment]) -> str:
    if treatment is None or treatment.assigned is None:
        return ""

    return treatment.assigned


def get_zr_index_key(current_value: Vulnerability) -> PrimaryKey:
    return keys.build_key(
        facet=ZR_INDEX_METADATA,
        values={
            "finding_id": current_value.finding_id,
            "vuln_id": current_value.id,
            "is_deleted": str(
                current_value.state.status is VulnerabilityStateStatus.DELETED
            ).lower(),
            "is_zero_risk": str(
                bool(
                    current_value.zero_risk
                    and current_value.zero_risk.status in ZR_FILTER_STATUSES
                )
            ).lower(),
            "state_status": str(current_value.state.status.value).lower(),
            "verification_status": str(
                current_value.verification
                and current_value.verification.status.value
            ).lower(),
        },
    )


def get_new_zr_index_key(
    current_value: Vulnerability, entry: VulnerabilityHistoricEntry
) -> Optional[PrimaryKey]:
    new_zr_index_key = None
    if isinstance(entry, VulnerabilityState):
        new_zr_index_key = keys.build_key(
            facet=ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    entry.status is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": str(entry.status.value).lower(),
                "verification_status": str(
                    current_value.verification
                    and current_value.verification.status.value
                ).lower(),
            },
        )
    if isinstance(entry, VulnerabilityZeroRisk):
        new_zr_index_key = keys.build_key(
            facet=ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    current_value.state.status
                    is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_zero_risk": str(
                    entry.status in ZR_FILTER_STATUSES
                ).lower(),
                "state_status": str(current_value.state.status.value).lower(),
                "verification_status": str(
                    current_value.verification
                    and current_value.verification.status.value
                ).lower(),
            },
        )
    if isinstance(entry, VulnerabilityVerification):
        new_zr_index_key = keys.build_key(
            facet=ZR_INDEX_METADATA,
            values={
                "finding_id": current_value.finding_id,
                "vuln_id": current_value.id,
                "is_deleted": str(
                    current_value.state.status
                    is VulnerabilityStateStatus.DELETED
                ).lower(),
                "is_zero_risk": str(
                    bool(
                        current_value.zero_risk
                        and current_value.zero_risk.status
                        in ZR_FILTER_STATUSES
                    )
                ).lower(),
                "state_status": str(current_value.state.status.value).lower(),
                "verification_status": str(entry.status.value).lower(),
            },
        )

    return new_zr_index_key
