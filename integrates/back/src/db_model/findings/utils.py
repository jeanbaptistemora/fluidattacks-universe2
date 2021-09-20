from .enums import (
    FindingStateJustification,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from .types import (
    Finding,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingVerification,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Optional,
    Set,
    Tuple,
)


def filter_non_state_status_findings(
    findings: Tuple[Finding, ...], status: Set[FindingStateStatus]
) -> Tuple[Finding, ...]:
    return tuple(
        finding for finding in findings if finding.state.status not in status
    )


def format_evidences_item(evidences: FindingEvidences) -> Item:
    return {
        field: evidence._asdict()
        for field, evidence in evidences._asdict().items()
        if evidence is not None
    }


def format_state(state_item: Item) -> FindingState:
    return FindingState(
        justification=FindingStateJustification[state_item["justification"]],
        modified_by=state_item["modified_by"],
        modified_date=state_item["modified_date"],
        source=Source[state_item["source"]],
        status=FindingStateStatus[state_item["status"]],
    )


def format_state_item(state: FindingState) -> Item:
    return {
        "justification": state.justification.value,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "source": state.source.value,
        "status": state.status.value,
    }


def format_treatment_summary_item(
    treatment_summary: FindingTreatmentSummary,
) -> Item:
    return {
        "accepted": treatment_summary.accepted,
        "accepted_undefined": treatment_summary.accepted_undefined,
        "in_progress": treatment_summary.in_progress,
        "new": treatment_summary.new,
    }


def format_treatment_summary(
    treatment_summary_item: Item,
) -> FindingTreatmentSummary:
    return FindingTreatmentSummary(
        accepted=int(treatment_summary_item["accepted"]),
        accepted_undefined=int(treatment_summary_item["accepted_undefined"]),
        in_progress=int(treatment_summary_item["in_progress"]),
        new=int(treatment_summary_item["new"]),
    )


def format_unreliable_indicators_item(
    indicators: FindingUnreliableIndicators,
) -> Item:
    return {
        "unreliable_closed_vulnerabilities": (
            indicators.unreliable_closed_vulnerabilities
        ),
        "unreliable_is_verified": indicators.unreliable_is_verified,
        "unreliable_newest_vulnerability_report_date": (
            indicators.unreliable_newest_vulnerability_report_date
        ),
        "unreliable_oldest_open_vulnerability_report_date": (
            indicators.unreliable_oldest_open_vulnerability_report_date
        ),
        "unreliable_oldest_vulnerability_report_date": (
            indicators.unreliable_oldest_vulnerability_report_date
        ),
        "unreliable_open_vulnerabilities": (
            indicators.unreliable_open_vulnerabilities
        ),
        "unreliable_status": indicators.unreliable_status.value,
        "unreliable_where": indicators.unreliable_where,
        "unreliable_treatment_summary": format_treatment_summary_item(
            indicators.unreliable_treatment_summary
        ),
    }


def format_unreliable_indicators(
    indicators_item: Item,
) -> FindingUnreliableIndicators:
    return FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=int(
            indicators_item["unreliable_closed_vulnerabilities"]
        ),
        unreliable_is_verified=indicators_item["unreliable_is_verified"],
        unreliable_newest_vulnerability_report_date=(
            indicators_item["unreliable_newest_vulnerability_report_date"]
        ),
        unreliable_oldest_open_vulnerability_report_date=(
            indicators_item["unreliable_oldest_open_vulnerability_report_date"]
        ),
        unreliable_oldest_vulnerability_report_date=(
            indicators_item["unreliable_oldest_vulnerability_report_date"]
        ),
        unreliable_open_vulnerabilities=int(
            indicators_item["unreliable_open_vulnerabilities"]
        ),
        unreliable_status=FindingStatus[indicators_item["unreliable_status"]],
        unreliable_where=indicators_item["unreliable_where"],
        unreliable_treatment_summary=format_treatment_summary(
            indicators_item["unreliable_treatment_summary"]
        ),
    )


def format_verification(verification_item: Item) -> FindingVerification:
    return FindingVerification(
        comment_id=verification_item["comment_id"],
        modified_by=verification_item["modified_by"],
        modified_date=verification_item["modified_date"],
        status=FindingVerificationStatus[verification_item["status"]],
        vulnerability_ids=verification_item["vulnerability_ids"],
    )


def format_verification_item(verification: FindingVerification) -> Item:
    return {
        "comment_id": verification.comment_id,
        "modified_by": verification.modified_by,
        "modified_date": verification.modified_date,
        "status": verification.status.value,
        "vulnerability_ids": verification.vulnerability_ids,
    }


def format_optional_state(
    state_item: Item,
) -> Optional[FindingState]:
    state = None
    if state_item.get("status"):
        state = format_state(state_item)
    return state


def format_optional_verification(
    verification_item: Item,
) -> Optional[FindingVerification]:
    verification = None
    if verification_item.get("status"):
        verification = format_verification(verification_item)
    return verification


def format_optional_state_item(
    state: Optional[FindingState],
) -> Item:
    state_item = {}
    if state is not None:
        state_item = format_state_item(state)
    return state_item


def format_optional_verification_item(
    verification: Optional[FindingVerification],
) -> Item:
    verification_item = {}
    if verification is not None:
        verification_item = format_verification_item(verification)
    return verification_item


def get_latest_verification(
    historic_verification: Tuple[FindingVerification, ...]
) -> Optional[FindingVerification]:
    verification = None
    if historic_verification:
        verification = max(
            historic_verification,
            key=lambda verification: datetime.fromisoformat(
                verification.modified_date
            ),
        )
    return verification
