from custom_exceptions import (
    DocumentNotFound,
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
    logs as logs_utils,
)


@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def resolve(
    parent: Organization,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> str:
    logs_utils.cloudwatch_log(
        info.context,
        "Security: Attempted to get vulnerabilities for organization"
        f": {parent.id} at {datetime_utils.get_now()}",
    )

    if parent.vulnerabilities_url is None:
        raise DocumentNotFound()

    logs_utils.cloudwatch_log(
        info.context,
        "Security: Get vulnerabilities for organization"
        f": {parent.id} at {datetime_utils.get_now()}",
    )
    return parent.vulnerabilities_url
