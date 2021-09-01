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
    RootItem,
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


async def deactivate_root(
    info: GraphQLResolveInfo,
    root: RootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    if await roots_domain.has_open_vulns(
        root, info.context.loaders, kwargs["group_name"]
    ):
        raise HasOpenVulns()
    await roots_domain.deactivate_root(
        group_name=kwargs["group_name"],
        other=kwargs.get("other") if kwargs["reason"] == "OTHER" else None,
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
        await require_service_white(deactivate_root)(
            info, root, user_email, **kwargs
        )
    else:
        await require_service_black(deactivate_root)(
            info, root, user_email, **kwargs
        )

    return SimplePayload(success=True)
