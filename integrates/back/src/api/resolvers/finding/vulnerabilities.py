from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
    Tuple,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader = info.context.loaders.finding_vulnerabilities_nzr
    vulns_nzr: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        parent.id
    )
    if not kwargs.get("state"):
        return list(vulns_nzr)

    try:
        filter_status = VulnerabilityStateStatus[
            str(kwargs.get("state")).upper()
        ]
        return [
            vuln for vuln in vulns_nzr if vuln.state.status == filter_status
        ]
    except KeyError:
        return []
