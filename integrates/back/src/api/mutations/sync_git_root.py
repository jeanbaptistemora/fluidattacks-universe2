from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.actions import (
    clone_roots,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRootItem,
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
    token as token_utils,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    group_name = kwargs["group_name"]
    root: GitRootItem = await loaders.root.load(
        (group_name, kwargs["root_id"])
    )
    await clone_roots.queue_sync_git_roots(
        loaders=loaders,
        roots=(root,),
        user_email=user_email,
        group_name=root.group_name,
        force=True,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Queued a sync clone for root {root.state.nickname} in "
        f"{group_name} by {user_email}",
    )

    return SimplePayload(success=True)
