from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
)
from custom_types import (
    Vulnerability,
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
    vuln_commit: str,
    vuln_id: str,
    vuln_where: str,
    vuln_specific: str,
    vuln_type: str,
) -> bool:
    if vuln_type != "lines":
        raise ExpectedVulnToBeOfLinesType.new()

    validate_commit_hash(vuln_commit)
    validate_specific(vuln_specific)
    validate_uniqueness(
        finding_vulns_data=finding_vulns_data,
        vuln_where=vuln_where,
        vuln_specific=vuln_specific,
        vuln_type=vuln_type,
    )
    validate_where(vuln_where)

    return await update(
        finding_id=finding_id,
        vuln_id=vuln_id,
        data={
            "commit_hash": vuln_commit,
            "where": vuln_where,
            "specific": vuln_specific,
        },
    )
