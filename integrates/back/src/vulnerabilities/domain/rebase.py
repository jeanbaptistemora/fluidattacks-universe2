from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
)
from custom_types import (
    Vulnerability,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from typing import (
    List,
)
from vulnerabilities.dal import (
    update,
)
from vulnerabilities.domain.validations import (
    validate_commit_hash,
    validate_specific,
    validate_uniqueness,
    validate_where,
)


async def rebase(
    *,
    finding_id: str,
    finding_vulns_data: List[Vulnerability],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> bool:
    if vulnerability_type != VulnerabilityType.LINES:
        raise ExpectedVulnToBeOfLinesType.new()

    validate_commit_hash(vulnerability_commit)
    validate_specific(vulnerability_specific)
    validate_uniqueness(
        finding_vulns_data=finding_vulns_data,
        vulnerability_where=vulnerability_where,
        vulnerability_specific=vulnerability_specific,
        vulnerability_type=vulnerability_type,
    )
    validate_where(vulnerability_where)

    return await update(
        finding_id=finding_id,
        vuln_id=vulnerability_id,
        data={
            "commit_hash": vulnerability_commit,
            "where": vulnerability_where,
            "specific": vulnerability_specific,
        },
    )
