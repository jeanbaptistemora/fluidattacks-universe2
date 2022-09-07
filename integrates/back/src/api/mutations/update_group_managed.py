# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupManaged,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    turn_args_into_kwargs,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
@turn_args_into_kwargs
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    managed: GroupManaged,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    managed = GroupManaged(managed)
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]

    await groups_domain.update_group_managed(
        loaders=loaders,
        comments=comments,
        group_name=group_name,
        managed=managed,
        user_email=user_email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Updated managed in group {group_name} successfully",
    )

    return SimplePayload(success=True)
