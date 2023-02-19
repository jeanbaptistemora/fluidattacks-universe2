from .payloads.types import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    PermissionDenied,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateJustification,
    GroupSubscriptionType,
    GroupTier,
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
)
from sessions import (
    domain as sessions_domain,
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
    _: None,
    info: GraphQLResolveInfo,
    comments: str,
    group_name: str,
    reason: str,
    subscription: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await sessions_domain.get_jwt_content(info.context)
    email = user_info["user_email"]
    has_arm: bool = kwargs["has_asm"]
    has_machine: bool = kwargs["has_machine"]
    has_squad: bool = kwargs["has_squad"]
    subscription_type = GroupSubscriptionType[subscription.upper()]
    if kwargs.get("service"):
        service = GroupService[str(kwargs["service"]).upper()]
    else:
        service = (
            GroupService.WHITE
            if subscription_type == GroupSubscriptionType.CONTINUOUS
            else GroupService.BLACK
        )
    tier = GroupTier[str(kwargs.get("tier", "free")).upper()]

    try:
        await groups_domain.update_group(
            loaders=loaders,
            comments=comments,
            email=email,
            group_name=group_name,
            justification=GroupStateJustification[reason.upper()],
            has_arm=has_arm,
            has_machine=has_machine,
            has_squad=has_squad,
            service=service,
            subscription=subscription_type,
            tier=tier,
        )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted "
            f"to update {group_name} group",
        )
        raise

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Updated group {group_name} successfully",
    )

    return SimplePayload(success=True)
