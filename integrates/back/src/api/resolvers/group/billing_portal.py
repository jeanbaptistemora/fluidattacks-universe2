from billing import (
    domain as billing_domain,
)
from billing.types import (
    Portal,
)
from custom_types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from organizations import (
    domain as orgs_domain,
)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    parent: Group, _info: GraphQLResolveInfo, **_kwargs: None
) -> Portal:
    group_name: str = parent["name"]
    org_id: str = await orgs_domain.get_id_for_group(group_name)
    org_name: str = await orgs_domain.get_name_by_id(org_id)

    return await billing_domain.portal(
        org_name=org_name,
        group_name=group_name,
    )
