from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    clean_up_kwargs,
    resolve_kwargs,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    image: Optional[UploadFile] = None,
    file: Optional[UploadFile] = None,
    **kwargs: Any,
) -> SimplePayload:
    """Resolve create_event mutation."""
    group_name: str = resolve_kwargs(kwargs)
    kwargs = clean_up_kwargs(kwargs)
    user_info = await token_utils.get_jwt_content(info.context)
    analyst_email = user_info["user_email"]
    success = await events_domain.create_event(
        info.context.loaders,
        analyst_email,
        group_name.lower(),
        file,
        image,
        **kwargs,
    )
    if success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Created event in {group_name} project successfully",
        )
        redis_del_by_deps_soon("create_event", group_name=group_name)

    return SimplePayload(success=success)
