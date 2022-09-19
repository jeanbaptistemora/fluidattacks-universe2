# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupStateRemovalJustification,
    GroupTier,
)
from db_model.groups.types import (
    Group,
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
    token as token_utils,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
    group_name: str,
    reason: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    group: Group = await loaders.group.load(group_name)
    requester_email = user_info["user_email"]

    try:
        await groups_domain.update_group(
            loaders=loaders,
            comments="",
            group_name=group_name,
            justification=GroupStateRemovalJustification[reason.upper()],
            has_asm=False,
            has_machine=False,
            has_squad=False,
            service=group.state.service,
            subscription=group.state.type,
            tier=GroupTier.FREE,
            user_email=requester_email,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted "
            f"to remove {group_name} group",
        )
        raise
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context, f"Security: Attempted to remove group {group_name}"
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed group {group_name} successfully",
    )

    return SimplePayload(success=True)
