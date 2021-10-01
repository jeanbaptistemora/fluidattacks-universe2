from aiodataloader import (
    DataLoader,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    HasOpenVulns,
)
from custom_types import (
    SimplePayload,
)
from db_model.roots.types import (
    GitRootItem,
    IPRootItem,
    URLRootItem,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
    require_service_white,
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


@require_service_white
async def deactivate_git_root(
    _info: GraphQLResolveInfo,
    root: GitRootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    if await roots_domain.has_open_vulns(root):
        raise HasOpenVulns()
    await roots_domain.deactivate_root(
        group_name=kwargs["group_name"],
        other=kwargs.get("other"),
        reason=kwargs["reason"],
        root=root,
        user_email=user_email,
    )


@require_service_black
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


@require_service_black
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
    root_loader: DataLoader = info.context.loaders.root
    root = await root_loader.load((kwargs["group_name"], kwargs["id"]))

    if isinstance(root, GitRootItem):
        await deactivate_git_root(info, root, user_email, **kwargs)
    elif isinstance(root, IPRootItem):
        await deactivate_ip_root(info, root, user_email, **kwargs)
    else:
        await deactivate_url_root(info, root, user_email, **kwargs)

    return SimplePayload(success=True)
