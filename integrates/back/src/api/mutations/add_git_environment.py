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
from sessions.domain import (
    get_jwt_content,
)
from typing import (
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_white
)
async def mutate(  # pylint: disable = too-many-arguments
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    url: str,
    url_type: str,
    root_id: str,
    cloud_name: Optional[str] = None,
    **_kwargs: None,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info = await get_jwt_content(info.context)
    user_email = user_info["user_email"]
    await roots_domain.add_root_environment_url(
        loaders=loaders,
        group_name=group_name,
        root_id=root_id,
        url=url,
        url_type=url_type,
        user_email=user_email,
        should_notified=True,
        cloud_type=cloud_name,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Updated git envs for root {root_id}"
    )

    return SimplePayload(success=True)
