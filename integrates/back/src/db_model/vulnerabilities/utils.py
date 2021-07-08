from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityApprovalStatus,
    VulnerabilityDeletionJustification,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from .types import (
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.enums import (
    Source,
)
from dynamodb.types import (
    Item,
)


def format_state(item: Item) -> VulnerabilityState:
    return VulnerabilityState(
        approval_status=VulnerabilityApprovalStatus[item["approval_status"]]
        if "approval_status" in item
        else None,
        justification=VulnerabilityDeletionJustification[item["justification"]]
        if "justification" in item
        else None,
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        source=Source[item["source"]],
        status=VulnerabilityStateStatus[item["status"]],
    )


def format_state_item(state: VulnerabilityState) -> Item:
    return {
        "approval_status": state.approval_status.value
        if state.approval_status
        else None,
        "justification": state.justification.value
        if state.justification
        else None,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "source": state.source.value,
        "status": state.status.value,
    }


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=item.get("accepted_until", None),
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if "acceptance_status" in item
        else None,
        justification=item.get("justification", None),
        manager=item.get("manager", None),
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityTreatmentStatus[item["status"]],
    )


def format_treatment_item(state: VulnerabilityTreatment) -> Item:
    return {
        "accepted_until": state.accepted_until,
        "acceptance_status": state.acceptance_status.value
        if state.acceptance_status
        else None,
        "justification": state.justification,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_verification_item(state: VulnerabilityVerification) -> Item:
    return {
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }


def format_zero_risk(item: Item) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=item["comment_id"],
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        status=VulnerabilityZeroRiskStatus[item["status"]],
    )


def format_zero_risk_item(state: VulnerabilityZeroRisk) -> Item:
    return {
        "comment_id": state.comment_id,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }
