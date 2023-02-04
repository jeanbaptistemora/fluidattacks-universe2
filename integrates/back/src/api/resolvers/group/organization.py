from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations.utils import (
    get_organization,
)


async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
) -> str:
    loaders: Dataloaders = info.context.loaders
    org_id = parent.organization_id
    organization: Organization = await get_organization(loaders, org_id)
    organization_name = organization.name

    return organization_name
