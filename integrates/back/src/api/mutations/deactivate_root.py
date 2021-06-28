from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_drills_black,
    require_drills_white,
    require_login,
)
from dynamodb.types import (
    GitRootItem,
    IPRootItem,
    URLRootItem,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from roots import (
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
)


@require_drills_white
async def deactivate_git_root(
    _info: GraphQLResolveInfo,
    root: GitRootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.deactivate_root(
        group_name=kwargs["group_name"],
        other=kwargs.get("other"),
        reason=kwargs["reason"],
        root=root,
        user_email=user_email,
    )


@require_drills_black
async def deactivate_ip_root(
    _info: GraphQLResolveInfo,
    root: IPRootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.deactivate_root(
        group_name=kwargs["group_name"],
        other=kwargs.get("other"),
        reason=kwargs["reason"],
        root=root,
        user_email=user_email,
    )


@require_drills_black
async def deactivate_url_root(
    _info: GraphQLResolveInfo,
    root: URLRootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.deactivate_root(
        group_name=kwargs["group_name"],
        other=kwargs.get("other"),
        reason=kwargs["reason"],
        root=root,
        user_email=user_email,
    )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    root = await roots_domain.get_root(
        group_name=kwargs["group_name"], root_id=kwargs["id"]
    )

    if isinstance(root, GitRootItem):
        await deactivate_git_root(info, root, user_email, **kwargs)
    elif isinstance(root, IPRootItem):
        await deactivate_ip_root(info, root, user_email, **kwargs)
    else:
        await deactivate_url_root(info, root, user_email, **kwargs)

    return SimplePayload(success=True)
