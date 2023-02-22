from .schema import (
    FINDING,
)
from dataloaders import (
    Dataloaders,
)
from db_model.findings.types import (
    Finding,
)
from db_model.vulnerabilities.types import (
    FindingVulnerabilitiesRequest,
    VulnerabilitiesConnection,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@FINDING.field("draftsConnection")
@enforce_group_level_auth_async
async def resolve(
    parent: Finding,
    info: GraphQLResolveInfo,
    after: str | None = None,
    first: int | None = None,
    **_kwargs: None,
) -> VulnerabilitiesConnection:
    loaders: Dataloaders = info.context.loaders
    return await loaders.finding_vulnerabilities_draft_c.load(
        FindingVulnerabilitiesRequest(
            finding_id=parent.id,
            after=after,
            first=first,
            paginate=True,
        )
    )
