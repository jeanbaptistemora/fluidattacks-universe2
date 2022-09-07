# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aiodataloader import (
    DataLoader,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    Product,
)
from db_model.roots.enums import (
    RootStatus,
)
from db_model.roots.types import (
    GitRoot,
    IPRoot,
    URLRoot,
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
from unreliable_indicators.enums import (
    EntityDependency,
)
from unreliable_indicators.operations import (
    update_unreliable_indicators_by_deps,
)


@require_service_white
async def activate_git_root(
    info: GraphQLResolveInfo,
    root: GitRoot,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.activate_root(
        loaders=info.context.loaders,
        group_name=kwargs["group_name"],
        root=root,
        user_email=user_email,
    )


@require_service_black
async def activate_ip_root(
    info: GraphQLResolveInfo,
    root: IPRoot,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.activate_root(
        loaders=info.context.loaders,
        group_name=kwargs["group_name"],
        root=root,
        user_email=user_email,
    )


@require_service_black
async def activate_url_root(
    info: GraphQLResolveInfo,
    root: URLRoot,
    user_email: str,
    **kwargs: Any,
) -> None:
    await roots_domain.activate_root(
        loaders=info.context.loaders,
        group_name=kwargs["group_name"],
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

    if isinstance(root, GitRoot):
        await activate_git_root(info, root, user_email, **kwargs)
    elif isinstance(root, IPRoot):
        await activate_ip_root(info, root, user_email, **kwargs)
    else:
        await activate_url_root(info, root, user_email, **kwargs)

    await update_unreliable_indicators_by_deps(
        EntityDependency.activate_root,
        root_ids=[(root.group_name, root.id)],
    )

    if root.state.status != RootStatus.ACTIVE:
        if isinstance(root, GitRoot):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_LINES,
                entity=kwargs["group_name"],
                subject=user_email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
            )
        if isinstance(root, (GitRoot, URLRoot)):
            await batch_dal.put_action(
                action=Action.REFRESH_TOE_INPUTS,
                entity=kwargs["group_name"],
                subject=user_email,
                additional_info=root.state.nickname,
                product_name=Product.INTEGRATES,
            )

    return SimplePayload(success=True)
