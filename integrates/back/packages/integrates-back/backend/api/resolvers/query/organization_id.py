# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend.decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access
)
from backend.typing import Organization
from organizations import domain as orgs_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> Organization:
    name: str = kwargs['organization_name']
    organization: Organization = await orgs_domain.get_by_name(name)

    return organization
