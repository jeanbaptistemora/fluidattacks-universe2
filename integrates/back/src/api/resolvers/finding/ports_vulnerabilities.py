from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityType,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
)


async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **_kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader = info.context.loaders.finding_vulns_nzr_typed
    return [
        vuln
        for vuln in await finding_vulns_loader.load(parent.id)
        if vuln.type == VulnerabilityType.PORTS
    ]
