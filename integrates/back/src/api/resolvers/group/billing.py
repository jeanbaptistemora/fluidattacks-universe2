from billing import (
    domain as billing_domain,
)
from billing.types import (
    GroupBilling,
)
from datetime import (
    datetime,
)
from db_model.groups.types import (
    Group,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_login,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> GroupBilling:
    org: Organization = await info.context.loaders.organization.load(
        parent.organization_id,
    )
    return await billing_domain.get_group_billing(
        date=kwargs.get("date", datetime_utils.get_now()),
        org=org,
        group=parent,
        loaders=info.context.loaders,
    )
