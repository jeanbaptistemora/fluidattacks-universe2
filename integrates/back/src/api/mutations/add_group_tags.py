from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    ErrorUpdatingGroup,
)
from custom_types import (
    SimpleGroupPayload,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    tags: list[str],
) -> SimpleGroupPayload:
    loaders: Dataloaders = info.context.loaders
    group_name = group_name.lower()

    if not await groups_domain.is_valid_typed(loaders, group_name):
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to add tags without the allowed validations",
        )
        raise ErrorUpdatingGroup.new()

    if not await groups_domain.validate_group_tags(group_name, tags):
        logs_utils.cloudwatch_log(
            info.context,
            "Security: Attempted to add tags without allowed structure",
        )
        raise ErrorUpdatingGroup.new()

    group = await loaders.group_typed.load(group_name)
    await groups_domain.add_tags(group, set(tags))

    loaders.group_typed.clear(group_name)
    redis_del_by_deps_soon("add_group_tags", group_name=group_name)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Tags added to {group_name} group successfully",
    )

    group = await loaders.group_typed.load(group_name)
    return SimpleGroupPayload(success=True, group=group)
