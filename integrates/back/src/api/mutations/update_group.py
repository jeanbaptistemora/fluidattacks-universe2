from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from batch import (
    dal as batch_dal,
)
from batch.enums import (
    Product,
)
from custom_exceptions import (
    PermissionDenied,
)
from custom_types import (
    SimplePayload as SimplePayloadType,
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
    **parameters: Any,
) -> SimplePayloadType:
    loaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    requester_email = user_info["user_email"]
    success = False

    # Compatibility with old API
    has_asm: bool = parameters["has_asm"]
    has_machine: bool = parameters["has_machine"]
    has_squad: bool = parameters["has_squad"]

    try:
        success = await groups_domain.update_group_attrs(
            loaders=loaders,
            comments=comments,
            group_name=group_name,
            has_squad=has_squad,
            has_asm=has_asm,
            has_machine=has_machine,
            reason=reason,
            requester_email=requester_email,
            service=parameters.get(
                "service",
                ("WHITE" if subscription == "continuous" else "BLACK"),
            ),
            subscription=subscription,
            tier=parameters.get("tier", "free"),
        )
        if success and not has_asm:
            await batch_dal.put_action(
                action_name="remove_group_resources",
                entity=group_name,
                subject=requester_email,
                additional_info="mutation_update_group",
                queue="dedicated_later",
                product_name=Product.INTEGRATES,
            )
    except PermissionDenied:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Unauthorized role attempted to update group",
        )

    if success:
        loaders.group.clear(group_name)
        await redis_del_by_deps("update_group", group_name=group_name)
        await authz.revoke_cached_group_service_policies(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated group {group_name} successfully",
        )

    return SimplePayloadType(success=success)
