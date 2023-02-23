from .schema import (
    QUERY,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)


@QUERY.field("organizationId")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Organization | None:
    loaders: Dataloaders = info.context.loaders
    organization_name: str = kwargs["organization_name"]

    return await loaders.organization.load(organization_name)
