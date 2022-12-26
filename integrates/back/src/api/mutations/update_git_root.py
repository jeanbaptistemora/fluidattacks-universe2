from api.mutations import (
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
from db_model.roots.types import (
    GitRoot,
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
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_continuous
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    root = await roots_domain.update_git_root(
        info.context.loaders, user_email, **kwargs
    )
    if kwargs.get("credentials") and isinstance(root, GitRoot):
        with suppress(RootAlreadyCloning):
            await roots_domain.queue_sync_git_roots(
                loaders=info.context.loaders,
                roots=(root,),
                user_email=user_email,
                group_name=root.group_name,
            )

    info.context.loaders.root.clear((kwargs["group_name"], kwargs["id"]))
    info.context.loaders.group_roots.clear(kwargs["group_name"])
    logs_utils.cloudwatch_log(
        info.context, f'Security: Updated root {kwargs["id"]}'
    )

    return SimplePayload(success=True)
