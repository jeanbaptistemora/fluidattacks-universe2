from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesToReattackRequest,
    VulnerabilitiesConnection,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    Optional,
)


async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    after: Optional[str] = None,
    first: Optional[int] = None,
    **_kwargs: None,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders
    return await loaders.finding_vulnerabilities_to_reattack_c.load(
        FindingVulnerabilitiesToReattackRequest(
            finding_id=parent.id,
            after=after,
            first=first,
            paginate=True,
        )
    )
