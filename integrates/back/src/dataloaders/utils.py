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


def exists(key: str, item: Dict[str, Any]) -> bool:
    return key in item and item[key] is not None


def get_optional(key: str, item: Dict[str, Any], fallback: Any = None) -> Any:
    if exists(key, item):
        return item[key]
    return fallback


def format_vulnerability_state(state: Dict[str, Any]) -> VulnerabilityState:
    return VulnerabilityState(
        modified_by=state["analyst"],
        modified_date=state["date"],
        source=Source[map_source(state["source"]).upper()],
        status=VulnerabilityStateStatus[state["state"].upper()],
        justification=(
            VulnerabilityDeletionJustification[state["justification"]]
            if exists("justification", state)
            else None
        ),
    )


def format_vulnerability(item: Dict[str, Any]) -> Vulnerability:
    current_state: Dict[str, str] = item["historic_state"][-1]
    current_treatment: Optional[Dict[str, str]] = (
        item["historic_treatment"][-1]
        if exists("historic_treatment", item)
        else None
    )
    current_verification: Optional[Dict[str, str]] = (
        item["historic_verification"][-1]
        if exists("historic_verification", item)
        else None
    )
    current_zero_risk: Optional[Dict[str, str]] = (
        item["historic_zero_risk"][-1]
        if exists("historic_zero_risk", item)
        else None
    )

    return Vulnerability(
        finding_id=item["finding_id"],
        id=item["UUID"],
        specific=item["specific"],
        state=format_vulnerability_state(current_state),
        treatment=(
            VulnerabilityTreatment(
                modified_by=current_treatment["user"],
                modified_date=current_treatment["date"],
                status=VulnerabilityTreatmentStatus(
                    current_treatment["treatment"].replace(" ", "_").upper()
                ),
                accepted_until=get_optional(
                    "acceptance_date", current_treatment
                ),
                acceptance_status=(
                    VulnerabilityAcceptanceStatus[
                        current_treatment["acceptance_status"]
                    ]
                    if exists("acceptance_status", current_treatment)
                    else None
                ),
                justification=get_optional("justification", current_treatment),
                manager=get_optional("treatment_manager", current_treatment),
            )
            if current_treatment
            and current_treatment["treatment"].upper() != "NEW"
            else None
        ),
        type=VulnerabilityType(item["vuln_type"].upper()),
        where=item["where"],
        bug_tracking_system_url=get_optional("external_bts", item),
        commit=get_optional("commit_hash", item),
        custom_severity=(
            int(item["severity"]) if exists("severity", item) else None
        ),
        hash=None,
        repo=get_optional("repo_nickname", item),
        stream=item["stream"].split(",") if exists("stream", item) else None,
        tags=get_optional("tag", item),
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
