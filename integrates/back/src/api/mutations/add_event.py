from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleEventPayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
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
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    image: Optional[UploadFile] = None,
    file: Optional[UploadFile] = None,
    **kwargs: Any,
) -> SimpleEventPayload:
    """Resolve add_event mutation."""
    user_info = await token_utils.get_jwt_content(info.context)
    hacker_email = user_info["user_email"]
    event_payload = await events_domain.add_event(
        info.context.loaders,
        hacker_email=hacker_email,
        group_name=group_name.lower(),
        file=file,
        image=image,
        **kwargs,
    )
    if event_payload.success:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added a new event in {group_name} group successfully",
        )
        redis_del_by_deps_soon("add_event", group_name=group_name)

    return event_payload
