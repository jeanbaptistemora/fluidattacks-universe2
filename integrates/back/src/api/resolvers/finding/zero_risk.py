from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    Vulnerability,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    List,
    Tuple,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Finding, info: GraphQLResolveInfo, **kwargs: None
) -> List[Vulnerability]:
    finding_vulns_loader = info.context.loaders.finding_vulns_zr_typed
    vulns_zr: Tuple[Vulnerability, ...] = await finding_vulns_loader.load(
        parent.id
    )
    if not kwargs.get("state"):
        return list(vulns_zr)

    try:
        filter_status = VulnerabilityStateStatus[
            str(kwargs.get("state")).upper()
        ]
        return [
            vuln for vuln in vulns_zr if vuln.state.status == filter_status
        ]
    except KeyError:
        return []
