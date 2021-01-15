# Standard library
import logging
from typing import (
    Any,
    cast,
    Set
)

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from back.settings import LOGGING

from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_integrates
)
from backend.domain import project as group_domain
from backend.typing import SimpleProjectPayload as SimpleProjectPayloadType


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates
)
async def mutate(  # pylint: disable=too-many-arguments
    _: Any,
    info: GraphQLResolveInfo,
    project_name: str,
    tag: str
) -> SimpleProjectPayloadType:
    success = False
    group_name = project_name.lower()
    group_loader = info.context.loaders['group']
    if await group_domain.is_alive(group_name):
        project_attrs = await group_loader.load(group_name)
        project_tags = {'tag': project_attrs['tags']}
        cast(Set[str], project_tags.get('tag')).remove(tag)
        if project_tags.get('tag') == set():
            project_tags['tag'] = None
        tag_deleted = await group_domain.update(group_name, project_tags)
        if tag_deleted:
            success = True
        else:
            LOGGER.error('Couldn\'t remove a tag', extra={'extra': locals()})
    if success:
        util.queue_cache_invalidation(f'tags*{group_name}')
        group_loader.clear(group_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Removed tag from {group_name} group successfully'
        )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to remove tag in {group_name} group'
        )

    group = await group_loader.load(group_name)
    return SimpleProjectPayloadType(success=success, project=group)
