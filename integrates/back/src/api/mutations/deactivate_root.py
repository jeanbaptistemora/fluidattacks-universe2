from aiodataloader import (
    DataLoader,
)
from aioextensions import (
    collect,
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
    dal as roots_dal,
    domain as roots_domain,
)
from typing import (
    Any,
    Dict,
)
from vulnerabilities import (
    domain as vulns_domain,
)


async def deactivate_root(
    info: GraphQLResolveInfo,
    root: RootItem,
    user_email: str,
    **kwargs: Any,
) -> None:
    group_name: str = kwargs["group_name"]
    loaders = info.context.loaders
    reason: str = kwargs["reason"]

    if reason in {"OUT_OF_SCOPE", "REGISTERED_BY_MISTAKE"}:
        await collect(
            tuple(
                vulns_domain.close_by_exclusion(vuln)
                for vuln in await roots_dal.get_root_vulns(
                    loaders=loaders,
                    group_name=group_name,
                    nickname=root.state.nickname,
                )
            )
        )
    else:
        if await roots_domain.has_open_vulns(root, loaders, group_name):
            raise HasOpenVulns()

    await roots_domain.deactivate_root(
        group_name=group_name,
        other=kwargs.get("other") if reason == "OTHER" else None,
        reason=reason,
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
