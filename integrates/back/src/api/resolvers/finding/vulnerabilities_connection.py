from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.enums import (
    VulnerabilityStateStatus,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesZrRequest,
    VulnerabilitiesConnection,
    VulnerabilityFilters,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Any,
    Optional,
)


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> VulnerabilitiesConnection:
    after: Optional[str] = kwargs.get("after")
    first: Optional[int] = kwargs.get("first")
    state: Optional[str] = kwargs.get("state")
    where: Optional[str] = kwargs.get("where")
    loaders: Dataloaders = info.context.loaders

    return await loaders.finding_vulnerabilities_nzr_c.load(
        FindingVulnerabilitiesZrRequest(
            finding_id=parent.id,
            after=after,
            filters=VulnerabilityFilters(where=where),
            first=first,
            paginate=True,
            state_status=VulnerabilityStateStatus[state] if state else None,
        )
    )
