# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
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
from newutils.logs import (
    cloudwatch_log,
)
from newutils.token import (
    get_jwt_content,
)
from roots.domain import (
    update_url_root,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_service_black
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    root_id: str,
    nickname: str,
) -> SimplePayload:
    user_info: dict[str, str] = await get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await update_url_root(
        loaders=info.context.loaders,
        user_email=user_email,
        group_name=group_name.lower(),
        root_id=root_id,
        nickname=nickname,
    )

    cloudwatch_log(info.context, f"Security: Updated root {id}")

    return SimplePayload(success=True)
