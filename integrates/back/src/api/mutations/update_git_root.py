from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.actions import (
    clone_roots,
)
from batch.dal import (
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from contextlib import (
    suppress,
)
from custom_exceptions import (
    RootAlreadyCloning,
)
from custom_types import (
    SimplePayload,
)
from db_model.roots.types import (
    GitRoot,
    Root,
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
    require_login, enforce_group_level_auth_async, require_continuous
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    group_name: str = str(kwargs["group_name"]).lower()
    root_id: str = kwargs["id"]

    old_root: Root = await info.context.loaders.root.load(
        (group_name, root_id)
    )
    root = await roots_domain.update_git_root(
        info.context.loaders, user_email, **kwargs
    )
    if kwargs.get("credentials") and isinstance(root, GitRoot):
        with suppress(RootAlreadyCloning):
            await clone_roots.queue_sync_git_roots(
                loaders=info.context.loaders,
                roots=(root,),
                user_email=user_email,
                group_name=root.group_name,
            )
            await roots_domain.update_root_cloning_status(
                loaders=info.context.loaders,
                group_name=root.group_name,
                root_id=root.id,
                status="CLONING",
                message="Cloning in progress...",
            )

    nickname: str = kwargs.get("nickname") or old_root.state.nickname
    if nickname != old_root.state.nickname:
        await put_action(
            action=Action.UPDATE_NICKNAME,
            additional_info=group_name,
            attempt_duration_seconds=3600,
            entity=root_id,
            memory=3800,
            product_name=Product.INTEGRATES,
            queue="unlimited_spot",
            subject=user_email,
            vcpus=2,
        )
    logs_utils.cloudwatch_log(
        info.context, f'Security: Updated root {kwargs["id"]}'
    )

    return SimplePayload(success=True)
