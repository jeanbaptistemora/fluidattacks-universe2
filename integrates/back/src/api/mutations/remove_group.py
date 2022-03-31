from api import (
    APP_EXCEPTIONS,
)
from ariadne.utils import (
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
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
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    reason: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    group: Group = await loaders.group_typed.load(group_name)
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
        await batch_dal.put_action(
            action=Action.REMOVE_GROUP_RESOURCES,
            entity=group_name,
            subject=requester_email,
            additional_info="mutation_remove_group",
            queue="dedicated_later",
            product_name=Product.INTEGRATES,
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

    redis_del_by_deps_soon("remove_group", group_name=group_name)
    await authz.revoke_cached_group_service_policies(group_name)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed group {group_name} successfully",
    )

    return SimplePayload(success=True)
