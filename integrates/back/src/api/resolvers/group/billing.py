from billing import (
    domain as billing_domain,
)
from billing.types import (
    GroupBilling,
)
from dataloaders import (
    Dataloaders,
)
from datetime import (
    datetime,
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
from newutils import (
    datetime as datetime_utils,
)
from organizations import (
    utils as orgs_utils,
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
    loaders: Dataloaders = info.context.loaders
    organization = await orgs_utils.get_organization(
        loaders, parent.organization_id
    )

    return await billing_domain.get_group_billing(
        date=kwargs.get("date", datetime_utils.get_now()),
        org=organization,
        group=parent,
        loaders=loaders,
    )
