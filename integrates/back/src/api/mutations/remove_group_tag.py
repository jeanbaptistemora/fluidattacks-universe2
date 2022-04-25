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
import logging
import logging.config
from newutils import (
    logs as logs_utils,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from typing import (
    Any,
)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_asm
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    group_name: str,
    tag: str,
) -> SimpleGroupPayload:
    group_name = group_name.lower()
    loaders: Dataloaders = info.context.loaders
    group = await loaders.group_typed.load(group_name)

    if await groups_domain.is_valid(loaders, group_name) and group.tags:
        await groups_domain.remove_tag(group=group, tag_to_remove=tag)
        redis_del_by_deps_soon("remove_group_tag", group_name=group_name)
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

    loaders.group_typed.clear(group_name)
    group = await loaders.group_typed.load(group_name)
    return SimpleGroupPayload(success=True, group=group)
