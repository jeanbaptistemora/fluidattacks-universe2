from .enums import (
    DraftRejectionReason,
    FindingCvssVersion,
    FindingSorts,
    FindingStateStatus,
    FindingStatus,
    FindingVerificationStatus,
)
from datetime import (
    datetime,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.findings.types import (
    DraftRejection,
    Finding,
    Finding20Severity,
    Finding31Severity,
    FindingEvidence,
    FindingEvidences,
    FindingState,
    FindingTreatmentSummary,
    FindingUnreliableIndicators,
    FindingUnreliableIndicatorsToUpdate,
    FindingVerification,
    FindingVerificationSummary,
)
from db_model.utils import (
    get_as_utc_iso_format,
)
from decimal import (
    Decimal,
)
from dynamodb.types import (
    Item,
)
from typing import (
    Iterable,
    Optional,
    Union,
)


def get_finding_inverted_state_converted(state: str) -> str:
    if state in {"CLOSED", "OPEN"}:
        translation: dict[str, str] = {
            "CLOSED": "SAFE",
            "OPEN": "VULNERABLE",
        }
        return translation[state]
    return state


def filter_non_state_status_findings(
    findings: Iterable[Finding], status: set[FindingStateStatus]
) -> tuple[Finding, ...]:
    return tuple(
        finding for finding in findings if finding.state.status not in status
    )


def has_rejected_drafts(*, drafts: Iterable[Finding]) -> bool:
    return bool(
        filter_non_state_status_findings(
            drafts,
            {
                FindingStateStatus.APPROVED,
                FindingStateStatus.CREATED,
                FindingStateStatus.DELETED,
                FindingStateStatus.MASKED,
                FindingStateStatus.SUBMITTED,
            },
        )
    )


def format_evidence(item: Item) -> FindingEvidence:
    return FindingEvidence(
        description=item["description"],
        modified_date=datetime.fromisoformat(item["modified_date"]),
        url=item["url"],
    )


def format_evidence_item(evidence: FindingEvidence) -> Item:
    return {
        "description": evidence.description,
        "modified_date": get_as_utc_iso_format(evidence.modified_date),
        "url": evidence.url,
    }


def format_evidences_item(evidences: FindingEvidences) -> Item:
    return {
        field: format_evidence_item(evidence)
        for field, evidence in evidences._asdict().items()
        if evidence is not None
    }


def format_finding(item: Item) -> Finding:
    state = format_state(item["state"])
    creation = format_state(item["creation"])
    submission = format_optional_state(item.get("submission"))
    approval = format_optional_state(item.get("approval"))
    verification = format_optional_verification(item.get("verification"))
    unreliable_indicators = format_unreliable_indicators(
        item["unreliable_indicators"]
    )

    if item["cvss_version"] == FindingCvssVersion.V31.value:
        severity: Union[
            Finding20Severity, Finding31Severity
        ] = Finding31Severity(
            **{
                field: Decimal(item["severity"][field])
                for field in Finding31Severity._fields
            }
        )
    else:
        severity = Finding20Severity(
            **{
                field: Decimal(item["severity"][field])
                for field in Finding20Severity._fields
            }
        )
    evidences = FindingEvidences(
        **{
            name: format_evidence(evidence)
            for name, evidence in item["evidences"].items()
        }
    )

    min_time_to_remediate: Optional[int] = None
    if "min_time_to_remediate" in item:
        min_time_to_remediate = int(item["min_time_to_remediate"])

    return Finding(
        hacker_email=item["analyst_email"],
        approval=approval,
        attack_vector_description=item["attack_vector_description"],
        creation=creation,
        description=item["description"],
        evidences=evidences,
        group_name=item["group_name"],
        id=item["id"],
        severity=severity,
        min_time_to_remediate=min_time_to_remediate,
        sorts=FindingSorts[item["sorts"]],
        submission=submission,
        recommendation=item["recommendation"],
        requirements=item["requirements"],
        title=item["title"],
        threat=item["threat"],
        state=state,
        unfulfilled_requirements=item.get("unfulfilled_requirements", []),
        unreliable_indicators=unreliable_indicators,
        verification=verification,
    )


def format_state(state_item: Item) -> FindingState:
    return FindingState(
        justification=StateRemovalJustification[state_item["justification"]],
        modified_by=state_item["modified_by"],
        modified_date=datetime.fromisoformat(state_item["modified_date"]),
        rejection=format_rejection(state_item.get("rejection", None)),
        source=Source[state_item["source"]],
        status=FindingStateStatus[state_item["status"]],
    )


def format_state_item(state: FindingState) -> Item:
    return {
        "justification": state.justification.value,
        "modified_by": state.modified_by,
        "modified_date": get_as_utc_iso_format(state.modified_date),
        "rejection": format_rejection_item(state.rejection),
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
        "untreated": treatment_summary.untreated,
    }


def format_treatment_summary(
    treatment_summary_item: Item,
) -> FindingTreatmentSummary:

    return FindingTreatmentSummary(
        accepted=int(treatment_summary_item["accepted"]),
        accepted_undefined=int(treatment_summary_item["accepted_undefined"]),
        in_progress=int(treatment_summary_item["in_progress"]),
        untreated=int(
            treatment_summary_item.get(
                "new", treatment_summary_item.get("untreated", 0)
            )
        ),
    )


def format_verification_summary_item(
    treatment_summary: FindingVerificationSummary,
) -> Item:
    return {
        "requested": treatment_summary.requested,
        "on_hold": treatment_summary.on_hold,
        "verified": treatment_summary.verified,
    }


def format_verification_summary(
    verification_summary_item: Item,
) -> FindingVerificationSummary:
    return FindingVerificationSummary(
        requested=int(verification_summary_item["requested"]),
        on_hold=int(verification_summary_item["on_hold"]),
        verified=int(verification_summary_item["verified"]),
    )


def format_unreliable_indicators_item(
    indicators: FindingUnreliableIndicators,
) -> Item:
    item = {
        "unreliable_closed_vulnerabilities": (
            indicators.unreliable_closed_vulnerabilities
        ),
        "unreliable_newest_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_newest_vulnerability_report_date
            )
            if indicators.unreliable_newest_vulnerability_report_date
            else None
        ),
        "unreliable_oldest_open_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_oldest_open_vulnerability_report_date
            )
            if indicators.unreliable_oldest_open_vulnerability_report_date
            else None
        ),
        "unreliable_oldest_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_oldest_vulnerability_report_date
            )
            if indicators.unreliable_oldest_vulnerability_report_date
            else None
        ),
        "unreliable_open_vulnerabilities": (
            indicators.unreliable_open_vulnerabilities
        ),
        "unreliable_status": indicators.unreliable_status.value,
        "unreliable_where": indicators.unreliable_where,
        "unreliable_treatment_summary": format_treatment_summary_item(
            indicators.unreliable_treatment_summary
        ),
        "unreliable_verification_summary": format_verification_summary_item(
            indicators.unreliable_verification_summary
        ),
    }

    return {key: value for key, value in item.items() if value is not None}


def format_unreliable_indicators_to_update_item(
    indicators: FindingUnreliableIndicatorsToUpdate,
) -> Item:
    item = {
        "unreliable_closed_vulnerabilities": (
            indicators.unreliable_closed_vulnerabilities
        ),
        "unreliable_newest_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_newest_vulnerability_report_date
            )
            if indicators.unreliable_newest_vulnerability_report_date
            else None
        ),
        "unreliable_oldest_open_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_oldest_open_vulnerability_report_date
            )
            if indicators.unreliable_oldest_open_vulnerability_report_date
            else None
        ),
        "unreliable_oldest_vulnerability_report_date": (
            get_as_utc_iso_format(
                indicators.unreliable_oldest_vulnerability_report_date
            )
            if indicators.unreliable_oldest_vulnerability_report_date
            else None
        ),
        "unreliable_open_vulnerabilities": (
            indicators.unreliable_open_vulnerabilities
        ),
        "unreliable_status": indicators.unreliable_status,
        "unreliable_where": indicators.unreliable_where,
        "unreliable_treatment_summary": format_treatment_summary_item(
            indicators.unreliable_treatment_summary
        )
        if indicators.unreliable_treatment_summary
        else None,
        "unreliable_verification_summary": format_verification_summary_item(
            indicators.unreliable_verification_summary
        )
        if indicators.unreliable_verification_summary
        else None,
    }
    item = {key: value for key, value in item.items() if value is not None}

    if indicators.clean_unreliable_newest_vulnerability_report_date:
        item["unreliable_newest_vulnerability_report_date"] = None
    if indicators.clean_unreliable_oldest_open_vulnerability_report_date:
        item["unreliable_oldest_open_vulnerability_report_date"] = None
    if indicators.clean_unreliable_oldest_vulnerability_report_date:
        item["unreliable_oldest_vulnerability_report_date"] = None

    return item


def format_unreliable_indicators(
    indicators_item: Item,
) -> FindingUnreliableIndicators:
    return FindingUnreliableIndicators(
        unreliable_closed_vulnerabilities=int(
            indicators_item["unreliable_closed_vulnerabilities"]
        ),
        unreliable_newest_vulnerability_report_date=(
            datetime.fromisoformat(
                indicators_item["unreliable_newest_vulnerability_report_date"]
            )
            if indicators_item.get(
                "unreliable_newest_vulnerability_report_date"
            )
            else None
        ),
        unreliable_oldest_open_vulnerability_report_date=(
            datetime.fromisoformat(
                indicators_item[
                    "unreliable_oldest_open_vulnerability_report_date"
                ]
            )
            if indicators_item.get(
                "unreliable_oldest_open_vulnerability_report_date"
            )
            else None
        ),
        unreliable_oldest_vulnerability_report_date=(
            datetime.fromisoformat(
                indicators_item["unreliable_oldest_vulnerability_report_date"]
            )
            if indicators_item.get(
                "unreliable_oldest_vulnerability_report_date"
            )
            else None
        ),
        unreliable_open_vulnerabilities=int(
            indicators_item["unreliable_open_vulnerabilities"]
        ),
        unreliable_status=FindingStatus[
            get_finding_inverted_state_converted(
                str(indicators_item["unreliable_status"]).upper()
            )
        ],
        unreliable_where=indicators_item["unreliable_where"],
        unreliable_treatment_summary=format_treatment_summary(
            indicators_item["unreliable_treatment_summary"]
        ),
        unreliable_verification_summary=format_verification_summary(
            indicators_item["unreliable_verification_summary"]
        ),
    )


def format_verification(verification_item: Item) -> FindingVerification:
    return FindingVerification(
        comment_id=verification_item["comment_id"],
        modified_by=verification_item["modified_by"],
        modified_date=datetime.fromisoformat(
            verification_item["modified_date"]
        ),
        status=FindingVerificationStatus[verification_item["status"]],
        vulnerability_ids=verification_item["vulnerability_ids"]
        if "vulnerability_ids" in verification_item
        else set(),
    )


def format_verification_item(verification: FindingVerification) -> Item:
    return {
        "comment_id": verification.comment_id,
        "modified_by": verification.modified_by,
        "modified_date": get_as_utc_iso_format(verification.modified_date),
        "status": verification.status.value,
        "vulnerability_ids": verification.vulnerability_ids
        if verification.vulnerability_ids
        else None,
    }


def format_optional_state(
    state_item: Optional[Item],
) -> Optional[FindingState]:
    state = None
    if state_item is not None:
        state = format_state(state_item)
    return state


def format_optional_verification(
    verification_item: Optional[Item],
) -> Optional[FindingVerification]:
    verification = None
    if verification_item is not None:
        verification = format_verification(verification_item)
    return verification


def format_rejection(
    rejection_item: Optional[Item],
) -> Optional[DraftRejection]:
    return (
        DraftRejection(
            other=rejection_item["other"],
            reasons={
                DraftRejectionReason[reason]
                for reason in rejection_item["reasons"]
            },
            rejected_by=rejection_item["rejected_by"],
            rejection_date=datetime.fromisoformat(
                rejection_item["rejection_date"]
            ),
            submitted_by=rejection_item["submitted_by"],
        )
        if rejection_item is not None
        else None
    )


def format_rejection_item(
    rejection: Optional[DraftRejection],
) -> Optional[Item]:
    return (
        {
            "other": rejection.other,
            "reasons": {str(reason.value) for reason in rejection.reasons},
            "rejected_by": rejection.rejected_by,
            "rejection_date": get_as_utc_iso_format(rejection.rejection_date),
            "submitted_by": rejection.submitted_by,
        }
        if rejection is not None
        else None
    )
