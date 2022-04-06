from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.actions import (
    clone_roots,
)
from custom_types import (
    AddRootPayload,
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
from roots import (
    domain as roots_domain,
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
) -> AddRootPayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    root: GitRootItem = await roots_domain.add_git_root(
        info.context.loaders, user_email, **kwargs
    )
    if kwargs.get("credentials"):
        await clone_roots.queue_sync_git_roots(
            loaders=info.context.loaders,
            roots=(root,),
            user_email=user_email,
            group_name=root.group_name,
        )
    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Added a root in {kwargs["group_name"].lower()}',
    )

    return AddRootPayload(root_id=root.id, success=True)
