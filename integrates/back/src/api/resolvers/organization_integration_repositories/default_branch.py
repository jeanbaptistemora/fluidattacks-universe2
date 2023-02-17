from .schema import (
    ORGANIZATION_INTEGRATION_REPOSITORIES,
)
from db_model.integration_repositories.types import (
    OrganizationIntegrationRepository,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@ORGANIZATION_INTEGRATION_REPOSITORIES.field("defaultBranch")
async def resolve(
    parent: OrganizationIntegrationRepository,
    _info: GraphQLResolveInfo,
) -> str:

    return parent.branch if parent.branch is not None else ""
