from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimpleProjectPayload as SimpleProjectPayloadType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
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
from newutils.utils import (
    resolve_kwargs,
)
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)
from settings import (
    LOGGING,
)
from typing import (
    Any,
    cast,
    Set,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login, enforce_group_level_auth_async, require_integrates
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any, info: GraphQLResolveInfo, tag: str, **kwargs: Any
) -> SimpleProjectPayloadType:
    success = False
    group_name = resolve_kwargs(kwargs).lower()
    group_loader = info.context.loaders.group
    if await groups_domain.is_alive(group_name):
        group_attrs = await group_loader.load(group_name)
        group_tags = {"tag": group_attrs["tags"]}
        cast(Set[str], group_tags.get("tag")).remove(tag)
        if group_tags.get("tag") == set():
            group_tags["tag"] = None
        tag_deleted = await groups_domain.update(group_name, group_tags)
        if tag_deleted:
            success = True
        else:
            LOGGER.error("Couldn't remove a tag", extra={"extra": locals()})
    if success:
        redis_del_by_deps_soon("remove_group_tag", group_name=group_name)
        group_loader.clear(group_name)
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Removed tag from {group_name} group successfully",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to remove tag in {group_name} group",
        )

    group = await group_loader.load(group_name)
    return SimpleProjectPayloadType(success=success, project=group)
