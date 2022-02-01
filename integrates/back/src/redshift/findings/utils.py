from datetime import (
    datetime,
)
from db_model.findings.enums import (
    FindingCvssVersion,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
    FindingState,
    FindingVerification,
)
from typing import (
    Any,
    Dict,
)


def format_row_metadata(
    finding: Finding,
) -> Dict[str, Any]:
    cvss_version = (
        FindingCvssVersion.V31
        if isinstance(finding.severity, Finding31Severity)
        else FindingCvssVersion.V20
    )
    return dict(
        id=finding.id,
        cvss_version=cvss_version.value,
        group_name=finding.group_name,
        hacker_email=finding.hacker_email,
        requirements=finding.requirements,
        sorts=finding.sorts.value,
        title=finding.title,
    )


def format_row_state(
    finding_id: str,
    state: FindingState,
) -> Dict[str, Any]:
    return dict(
        id=finding_id,
        modified_by=state.modified_by,
        modified_date=datetime.fromisoformat(state.modified_date),
        justification=state.justification.value,
        source=state.source.value,
        status=state.status.value,
    )


def format_row_verification(
    finding_id: str,
    verification: FindingVerification,
) -> Dict[str, Any]:
    return dict(
        id=finding_id,
        modified_date=datetime.fromisoformat(verification.modified_date),
        status=verification.status.value,
    )


def format_row_verification_vuln_ids(
    finding_id: str,
    modified_date: str,
    vulnerability_id: str,
) -> Dict[str, Any]:
    return dict(
        id=finding_id,
        modified_date=datetime.fromisoformat(modified_date),
        vulnerability_id=vulnerability_id,
    )
