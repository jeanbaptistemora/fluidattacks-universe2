from db_model.enums import (
    Source,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
    VulnerabilityDeletionJustification,
    VulnerabilityStateStatus,
    VulnerabilityTreatmentStatus,
    VulnerabilityType,
    VulnerabilityVerificationStatus,
    VulnerabilityZeroRiskStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from newutils.requests import (
    map_source,
)
from typing import (
    Any,
    Dict,
    Optional,
)


def format_vulnerability_state(state: Dict[str, Any]) -> VulnerabilityState:
    return VulnerabilityState(
        modified_by=state["analyst"],
        modified_date=state["date"],
        source=Source[map_source(state["source"]).upper()],
        status=VulnerabilityStateStatus[state["state"].upper()],
        justification=(
            VulnerabilityDeletionJustification[state["justification"]]
            if "justification" in state
            else None
        ),
    )


def format_vulnerability(item: Dict[str, Any]) -> Vulnerability:
    current_state: Dict[str, str] = item["historic_state"][-1]
    current_treatment: Dict[str, str] = item["historic_treatment"][-1]
    current_verification: Optional[Dict[str, str]] = (
        item["historic_verification"][-1]
        if "historic_verification" in item
        else None
    )
    current_zero_risk: Optional[Dict[str, str]] = (
        item["historic_zero_risk"][-1]
        if "historic_zero_risk" in item
        else None
    )

    return Vulnerability(
        finding_id=item["finding_id"],
        id=item["UUID"],
        specific=item["specific"],
        state=format_vulnerability_state(current_state),
        treatment=(
            None
            if current_treatment["treatment"].upper() == "NEW"
            else VulnerabilityTreatment(
                modified_by=current_treatment["user"],
                modified_date=current_treatment["date"],
                status=VulnerabilityTreatmentStatus(
                    current_treatment["treatment"].replace(" ", "_").upper()
                ),
                accepted_until=current_treatment.get("acceptance_date"),
                acceptance_status=(
                    VulnerabilityAcceptanceStatus[
                        current_treatment["acceptance_status"]
                    ]
                    if "acceptance_status" in current_treatment
                    else None
                ),
                justification=current_treatment.get("justification"),
                manager=current_treatment.get("treatment_manager"),
            )
        ),
        type=VulnerabilityType(item["vuln_type"].upper()),
        where=item["where"],
        bug_tracking_system_url=item.get("external_bts"),
        commit=item.get("commit_hash"),
        custom_severity=int(item["severity"]) if "severity" in item else None,
        hash=None,
        repo=item.get("repo_nickname"),
        stream=item["stream"].split(",") if "stream" in item else None,
        tags=item.get("tag"),
        verification=(
            VulnerabilityVerification(
                comment_id="",
                modified_by="",
                modified_date=current_verification["date"],
                status=VulnerabilityVerificationStatus(
                    current_verification["status"]
                ),
            )
            if current_verification
            else None
        ),
        zero_risk=(
            VulnerabilityZeroRisk(
                comment_id=current_zero_risk["comment_id"],
                modified_by=current_zero_risk["email"],
                modified_date=current_zero_risk["date"],
                status=VulnerabilityZeroRiskStatus(
                    current_zero_risk["status"]
                ),
            )
            if current_zero_risk
            else None
        ),
    )
