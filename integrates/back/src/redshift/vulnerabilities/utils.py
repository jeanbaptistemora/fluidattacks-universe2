from datetime import (
    datetime,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityState,
    VulnerabilityTreatment,
    VulnerabilityVerification,
    VulnerabilityZeroRisk,
)
from typing import (
    Any,
    Dict,
)


def format_row_metadata(
    vulnerability: Vulnerability,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability.id,
        custom_severity=vulnerability.custom_severity,
        finding_id=vulnerability.finding_id,
        skims_method=vulnerability.skims_method,
        type=vulnerability.type.value,
    )


def format_row_state(
    vulnerability_id: str,
    state: VulnerabilityState,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(state.modified_date),
        source=state.source.value,
        status=state.status.value,
    )


def format_row_treatment(
    vulnerability_id: str,
    treatment: VulnerabilityTreatment,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(treatment.modified_date),
        status=treatment.status.value,
        accepted_until=datetime.fromisoformat(treatment.accepted_until)
        if treatment.accepted_until
        else None,
        acceptance_status=treatment.acceptance_status.value
        if treatment.acceptance_status
        else None,
    )


def format_row_verification(
    vulnerability_id: str,
    verification: VulnerabilityVerification,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(verification.modified_date),
        status=verification.status.value,
    )


def format_row_zero_risk(
    vulnerability_id: str,
    zero_risk: VulnerabilityZeroRisk,
) -> Dict[str, Any]:
    return dict(
        id=vulnerability_id,
        modified_date=datetime.fromisoformat(zero_risk.modified_date),
        status=zero_risk.status.value,
    )
