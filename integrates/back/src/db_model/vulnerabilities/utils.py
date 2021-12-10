from .enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from .types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from dynamodb.types import (
    Item,
)


def format_vulnerability(item: Item) -> Vulnerability:
    state = format_state(item["state"])
    treatment = format_treatment(item["treatment"])
    verification = (
        format_verification(item["verification"])
        if "verification" in item
        else None
    )
    zero_risk = (
        format_zero_risk(item["zero_risk"]) if "zero_risk" in item else None
    )

    return Vulnerability(
        bug_tracking_system_url=item.get("bug_tracking_system_url", None),
        commit=item.get("commit", None),
        custom_severity=item.get("custom_severity", None),
        finding_id=item["finding_id"],
        hash=item.get("hash", None),
        repo=item.get("repo", None),
        skims_method=item.get("skims_method", None),
        specific=item["specific"],
        state=state,
        stream=item.get("stream", None),
        tags=item.get("tags", None),
        treatment=treatment,
        type=VulnerabilityType[item["type"]],
        id=item["id"],
        verification=verification,
        where=item["where"],
        zero_risk=zero_risk,
    )


def format_state(item: Item) -> VulnerabilityState:
    return VulnerabilityState(
        justification=StateRemovalJustification[item["justification"]]
        if item.get("justification", None)
        else None,
        modified_by=item["modified_by"],
        modified_date=item["modified_date"],
        source=Source[item["source"]],
        status=VulnerabilityStateStatus[item["status"]],
    )


def format_treatment(item: Item) -> VulnerabilityTreatment:
    return VulnerabilityTreatment(
        accepted_until=item.get("accepted_until", None),
        acceptance_status=VulnerabilityAcceptanceStatus[
            item["acceptance_status"]
        ]
        if item.get("acceptance_status", None)
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
        "manager": state.manager,
        "modified_by": state.modified_by,
        "modified_date": state.modified_date,
        "status": state.status.value,
    }


def format_verification(item: Item) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        modified_date=item["modified_date"],
        status=VulnerabilityVerificationStatus[item["status"]],
    )


def format_verification_item(state: VulnerabilityVerification) -> Item:
    return {
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
