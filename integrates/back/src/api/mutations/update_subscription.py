from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from custom_types import (
    Organization,
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
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
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group: Group = await loaders.group_typed.load(kwargs["group_name"])
    org_id: str = await orgs_domain.get_id_by_name(group.organization_name)
    org: Organization = await loaders.organization.load(org_id)

    # Update subscription
    result: bool = await billing_domain.update_subscription(
        subscription=kwargs["subscription"],
        org_billing_customer=org["billing_customer"],
        org_name=org["name"],
        group_name=group.name,
    )

    return SimplePayload(success=result)
