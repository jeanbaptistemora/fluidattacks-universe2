from .schema import (
    ORGANIZATION,
)
from billing import (
    domain as billing_domain,
)
from billing.types import (
    OrganizationBilling,
)
from datetime import (
    datetime,
)
from db_model.organizations.types import (
    Organization,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    datetime as datetime_utils,
)


@ORGANIZATION.field("billing")
@concurrent_decorators(
    enforce_organization_level_auth_async,
    require_login,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **kwargs: datetime,
) -> OrganizationBilling:
    return await billing_domain.get_organization_billing(
        date=kwargs.get("date", datetime_utils.get_now()),
        org=parent,
        loaders=info.context.loaders,
    )
