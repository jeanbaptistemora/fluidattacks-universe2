from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Action,
    Product,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.enums import (
    GroupService,
    GroupStateUpdationJustification,
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
    token as token_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps,
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
    reason: str,
    subscription: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    has_asm: bool = kwargs["has_asm"]
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
            group_name=group_name,
            justification=GroupStateUpdationJustification[reason.upper()],
            has_asm=has_asm,
            has_machine=has_machine,
            has_squad=has_squad,
            service=service,
            subscription=subscription_type,
            tier=tier,
            user_email=user_email,
        )
        if not has_asm:
            await batch_dal.put_action(
                action=Action.REMOVE_GROUP_RESOURCES,
                entity=group_name,
                subject=user_email,
                additional_info="mutation_update_group",
                queue="dedicated_later",
                product_name=Product.INTEGRATES,
            )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Unauthorized role attempted "
            f"to update {group_name} group",
        )
        raise

    await redis_del_by_deps("update_group", group_name=group_name)
    await authz.revoke_cached_group_service_policies(group_name)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Updated group {group_name} successfully",
    )

    return SimplePayload(success=True)
