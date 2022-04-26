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
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    after: Optional[str] = None,
    first: Optional[int] = None,
    state: Optional[str] = None,
    **_kwargs: None,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders
    return await loaders.finding_vulnerabilities_zr_c.load(
        FindingVulnerabilitiesZrRequest(
            finding_id=parent.id,
            after=after,
            first=first,
            paginate=True,
            state_status=VulnerabilityStateStatus[state] if state else None,
        )
    )
