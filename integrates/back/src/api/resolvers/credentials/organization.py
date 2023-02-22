from .schema import (
    CREDENTIALS,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    Credentials,
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


@CREDENTIALS.field("organization")
@require_organization_access
async def resolve(
    parent: Credentials,
    info: GraphQLResolveInfo,
) -> Organization | None:
    loaders: Dataloaders = info.context.loaders
    organization = await loaders.organization.load(parent.organization_id)
    return organization
