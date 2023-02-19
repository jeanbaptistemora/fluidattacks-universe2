from .payloads.types import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    RootAlreadyCloning,
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
    require_continuous,
    require_login,
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
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_continuous
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    root_id: str = kwargs["id"]
    group_name: str = kwargs["group_name"]
    user_info = await sessions_domain.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    root = await roots_domain.update_git_root(loaders, user_email, **kwargs)
    if kwargs.get("credentials") and isinstance(root, GitRoot):
        with suppress(RootAlreadyCloning):
            await roots_domain.queue_sync_git_roots(
                loaders=loaders,
                roots=(root,),
                user_email=user_email,
                group_name=root.group_name,
            )

    loaders.root.clear(RootRequest(group_name, root_id))
    loaders.group_roots.clear(group_name)
    logs_utils.cloudwatch_log(
        info.context, f"Security: Updated root {root_id}"
    )

    return SimplePayload(success=True)
