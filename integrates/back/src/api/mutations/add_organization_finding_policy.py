from .payloads.types import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
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
    logs as logs_utils,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_name: str,
    organization_name: str,
    tags: Optional[list[str]] = None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    await policies_domain.add_finding_policy(
        loaders=loaders,
        email=user_email,
        finding_name=finding_name.strip(),
        organization_name=organization_name,
        tags=set(tags) if tags is not None else set(),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added an org finding policy in {organization_name}",
    )

    return SimplePayload(success=True)
