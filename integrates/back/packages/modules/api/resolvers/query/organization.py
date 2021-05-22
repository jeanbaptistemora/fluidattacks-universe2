# None


from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import Organization
from decorators import (
    concurrent_decorators,
    require_login,
    require_organization_access,
)
from organizations import domain as orgs_domain


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: str
) -> Organization:
    org_id: str = kwargs["organization_id"]
    organization: Organization = await orgs_domain.get_by_id(org_id)
    return organization
