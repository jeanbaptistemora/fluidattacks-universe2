from db_model.findings.enums import (
    FindingCvssVersion,
)
from db_model.findings.types import (
    Finding,
    Finding31Severity,
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
