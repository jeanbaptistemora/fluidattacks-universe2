from db_model.enums import (
    Source,
    StateRemovalJustification,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityAcceptanceStatus,
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
from newutils.datetime import (
    convert_to_iso_str,
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
        modified_date=convert_to_iso_str(state["date"]),
        source=Source[map_source(state["source"]).upper()],
        status=VulnerabilityStateStatus[state["state"].upper()],
        justification=(
            StateRemovalJustification[state["justification"]]
            if exists("justification", state)
            else None
        ),
    )


def format_vulnerability_treatment(
    treatment: Dict[str, Any]
) -> VulnerabilityTreatment:
    accepted_until: Optional[str] = get_optional("acceptance_date", treatment)
    if accepted_until:
        accepted_until = convert_to_iso_str(accepted_until)
    return VulnerabilityTreatment(
        modified_by=get_optional("user", treatment),
        modified_date=convert_to_iso_str(treatment["date"]),
        status=VulnerabilityTreatmentStatus(
            treatment["treatment"].replace(" ", "_").upper()
        ),
        accepted_until=accepted_until,
        acceptance_status=(
            VulnerabilityAcceptanceStatus[treatment["acceptance_status"]]
            if exists("acceptance_status", treatment)
            else None
        ),
        justification=get_optional("justification", treatment),
        manager=get_optional("treatment_manager", treatment),
    )


def format_vulnerability_verification(
    verification: Dict[str, str]
) -> VulnerabilityVerification:
    return VulnerabilityVerification(
        comment_id="",
        modified_by="",
        modified_date=convert_to_iso_str(verification["date"]),
        status=VulnerabilityVerificationStatus(verification["status"]),
    )


def format_vulnerability_zero_risk(
    zero_risk: Dict[str, str]
) -> VulnerabilityZeroRisk:
    return VulnerabilityZeroRisk(
        comment_id=zero_risk["comment_id"],
        modified_by=zero_risk["email"],
        modified_date=convert_to_iso_str(zero_risk["date"]),
        status=VulnerabilityZeroRiskStatus(zero_risk["status"]),
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
            format_vulnerability_treatment(current_treatment)
            if current_treatment
            else None
        ),
        type=VulnerabilityType(item["vuln_type"].upper()),
        where=item["where"],
        bug_tracking_system_url=get_optional("external_bts", item),
        commit=get_optional("commit_hash", item),
        custom_severity=(
            int(item["severity"])
            if exists("severity", item) and item["severity"]
            else None
        ),
        hash=None,
        repo=get_optional("repo_nickname", item),
        stream=item["stream"].split(",") if exists("stream", item) else None,
        tags=sorted(item["tag"]) if exists("tag", item) else None,
        verification=(
            format_vulnerability_verification(current_verification)
            if current_verification
            else None
        ),
        zero_risk=(
            format_vulnerability_zero_risk(current_zero_risk)
            if current_zero_risk
            else None
        ),
    )
