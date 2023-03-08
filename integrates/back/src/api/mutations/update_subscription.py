from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from billing import (
    domain as billing_domain,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from organizations.utils import (
    get_organization,
)
from typing import (
    Any,
)


@MUTATION.field("updateSubscription")
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
    group = await groups_domain.get_group(loaders, kwargs["group_name"])
    org = await get_organization(loaders, group.organization_id)

    # Update subscription
    result: bool = await billing_domain.update_subscription(
        subscription=kwargs["subscription"],
        org_billing_customer=org.billing_customer,
        org_name=org.name,
        group_name=group.name,
    )

    return SimplePayload(success=result)
