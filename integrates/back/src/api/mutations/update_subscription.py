from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from custom_types import (
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
    org: dict[str, Any] = await loaders.organization.load(
        group.organization_id
    )

    # Update subscription
    result: bool = await billing_domain.update_subscription(
        subscription=kwargs["subscription"],
        org_billing_customer=str(org["billing_customer"]),
        org_name=str(org["name"]),
        group_name=group.name,
    )

    return SimplePayload(success=result)
