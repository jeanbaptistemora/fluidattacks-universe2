# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidRootType,
)
from dataloaders import (
    Dataloaders,
)
from db_model.roots.types import (
    IPRoot,
    Root,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_service_black,
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
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_black
)
@convert_kwargs_to_snake_case
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    url: str,
    url_type: str,
    root_id: str,
    **_kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    root: Root = await loaders.root.load((group_name, root_id))
    if not isinstance(root, IPRoot):
        raise InvalidRootType()
    await roots_domain.add_root_environment_url(
        loaders=loaders,
        group_name=group_name,
        root_id=root_id,
        url=url,
        url_type=url_type,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Added ip root environment for root {root_id}"
    )

    return SimplePayload(success=True)
