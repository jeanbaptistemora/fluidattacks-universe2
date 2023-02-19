from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    GitRoot,
    RootRequest,
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
    cast,
)


@MUTATION.field("syncGitRoot")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> SimplePayload:
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    group_name = kwargs["group_name"]
    git_root = cast(
        GitRoot,
        await loaders.root.load(RootRequest(group_name, kwargs["root_id"])),
    )
    await roots_domain.queue_sync_git_roots(
        loaders=loaders,
        roots=(git_root,),
        user_email=user_email,
        group_name=git_root.group_name,
        force=True,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Queued a sync clone for root {git_root.state.nickname} in "
        f"{group_name} by {user_email}",
    )

    return SimplePayload(success=True)
