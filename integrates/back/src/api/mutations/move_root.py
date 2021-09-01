from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
)
from custom_exceptions import (
    InvalidParameter,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
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


async def _move_root(
    context: Any,
    user_email: str,
    group_name: str,
    root_id: str,
    target_id: str,
) -> None:
    root_loader: DataLoader = context.root
    source_root = await root_loader.load((group_name, root_id))
    target_root = await root_loader.load((group_name, target_id))

    if (
        root_id == target_id
        or source_root.state.status != "ACTIVE"
        or target_root.state.status != "ACTIVE"
    ):
        raise InvalidParameter()

    await roots_domain.deactivate_root(
        group_name=group_name,
        other=target_id,
        reason="MOVED_TO_ANOTHER_ROOT",
        root=source_root,
        user_email=user_email,
    )
    await batch_dal.put_action(
        action_name="move_root",
        entity=source_root.state.nickname,
        subject=user_email,
        additional_info=target_root.state.nickname,
    )


@convert_kwargs_to_snake_case
@concurrent_decorators(require_login, enforce_group_level_auth_async)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await _move_root(
        info.context.loaders,
        user_email,
        kwargs["group_name"],
        kwargs["id"],
        kwargs["target_id"],
    )
    logs_utils.cloudwatch_log(
        info.context,
        f'Security: Moved a root in {kwargs["group_name"].lower()}',
    )

    return SimplePayload(success=True)
