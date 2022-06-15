from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credential,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@require_organization_access
async def resolve(
    parent: Credential,
    info: GraphQLResolveInfo,
) -> Organization:
    loaders: Dataloaders = info.context.loaders
    organization: Organization = await loaders.organization.load(
        parent.organization_id
    )
    return organization
