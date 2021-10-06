from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleGroupPayload as SimpleGroupPayloadType,
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
from newutils.utils import (
    get_key_or_fallback,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
    List,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: Any, info: GraphQLResolveInfo, tags: List[str], **kwargs: Any
) -> SimpleGroupPayloadType:
    success = False
    group_name = get_key_or_fallback(kwargs).lower()
    group_loader = info.context.loaders.group
    if await groups_domain.is_alive(group_name):
        if await groups_domain.validate_group_tags(group_name, tags):
            group_attrs = await group_loader.load(group_name)
            group_tags = {"tag": group_attrs["tags"]}
            success = await groups_domain.update_tags(
                group_name, group_tags, tags
            )
        else:
            logs_utils.cloudwatch_log(
                info.context,
                "Security: Attempted to add tags without allowed structure",
            )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to add tags without the allowed validations",
        )
    if success:
        group_loader.clear(group_name)
        info.context.loaders.group.clear(group_name)
        redis_del_by_deps_soon("add_group_tags", group_name=group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added tag to {group_name} group successfully",
        )

    group = await group_loader.load(group_name)
    return SimpleGroupPayloadType(success=success, group=group)
