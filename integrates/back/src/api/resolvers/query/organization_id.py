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
from organizations import (
    domain as orgs_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Organization:
    loaders: Dataloaders = info.context.loaders
    organization_name: str = kwargs["organization_name"]
    organization_id = await orgs_domain.get_id_by_name(organization_name)

    return await loaders.organization_typed.load(organization_id)
