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
from backend.domain import organization as org_domain
from backend.typing import Organization


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None,
    _info: GraphQLResolveInfo,
    **kwargs: str
) -> Organization:
    org_id: str = kwargs['organization_id']
    organization: Organization = await org_domain.get_by_id(org_id)

    return organization
