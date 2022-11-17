# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimpleGroupPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    tag: str,
) -> SimpleGroupPayload:
    group_name = group_name.lower()
    loaders: Dataloaders = info.context.loaders
    group = await loaders.group.load(group_name)
    user_info = await sessions_domain.get_jwt_content(info.context)
    email: str = user_info["user_email"]

    if await groups_domain.is_valid(loaders, group_name) and group.state.tags:
        await groups_domain.remove_tag(
            loaders=loaders,
            email=email,
            group=group,
            tag_to_remove=tag,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed tag from {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove tag in {group_name} group",
        )
        raise ErrorUpdatingGroup.new()

    loaders.group.clear(group_name)
    group = await loaders.group.load(group_name)

    return SimpleGroupPayload(success=True, group=group)
