from custom_exceptions import (
    ExpectedVulnToBeOfLinesType,
)
from vulnerabilities.dal import (
    update,
)
from vulnerabilities.domain.validations import (
    validate_commit_hash,
    validate_specific,
    validate_where,
)


async def rebase(
    *,
    finding_id: str,
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
