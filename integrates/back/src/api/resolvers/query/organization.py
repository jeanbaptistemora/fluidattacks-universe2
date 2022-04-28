# None


from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
)
async def resolve(
    _parent: None, _info: GraphQLResolveInfo, **kwargs: str
) -> Dict[str, Any]:
    org_id: str = kwargs["organization_id"]
    organization: Dict[str, Any] = await orgs_domain.get_by_id(org_id)
    return organization
