from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from roots import (
    domain as roots_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
    Optional,
)


@MUTATION.field("updateGitEnvironments")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    reason: Optional[str] = kwargs.get("reason", None)
    other: Optional[str] = kwargs.get("other") if reason == "OTHER" else None

    await roots_domain.update_git_environments(
        loaders=info.context.loaders,
        user_email=user_email,
        group_name=kwargs["group_name"],
        root_id=kwargs["id"],
        environment_urls=kwargs["environment_urls"],
        reason=reason,
        other=other,
    )
    logs_utils.cloudwatch_log(
        info.context, f'Security: Updated git envs for root {kwargs["id"]}'
    )

    return SimplePayload(success=True)
