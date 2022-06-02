from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
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
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    url: str,
    url_type: str,
    **kwargs: Any,
) -> SimplePayload:
    await roots_domain.add_git_environment_url(
        loaders=info.context.loaders,
        group_name=group_name,
        root_id=kwargs["id"],
        url=url,
        url_type=url_type,
    )
    logs_utils.cloudwatch_log(
        info.context, f'Security: Updated git envs for root {kwargs["id"]}'
    )

    return SimplePayload(success=True)
