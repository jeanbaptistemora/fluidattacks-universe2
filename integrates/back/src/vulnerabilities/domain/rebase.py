from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
    VulnerabilityMetadataToUpdate,
)
from typing import (
    Tuple,
)
from vulnerabilities.dal import (
    update_metadata,
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
    finding_vulns_data: Tuple[Vulnerability, ...],
    vulnerability_commit: str,
    vulnerability_id: str,
    vulnerability_where: str,
    vulnerability_specific: str,
    vulnerability_type: VulnerabilityType,
) -> None:
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

    await update_metadata(
        finding_id=finding_id,
        vulnerability_id=vulnerability_id,
        metadata=VulnerabilityMetadataToUpdate(
            commit=vulnerability_commit,
            specific=vulnerability_specific,
            where=vulnerability_where,
        ),
    )
