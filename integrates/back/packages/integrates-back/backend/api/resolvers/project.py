# Standard library  # pylint:disable=cyclic-import
# pylint:disable=too-many-lines
import logging
import sys
from typing import Set, Any, cast

# Third party libraries
from ariadne import (
    convert_kwargs_to_snake_case,
)
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_integrates
)
from backend.domain import (
    project as project_domain,
)
from backend.typing import (
    SimpleProjectPayload as SimpleProjectPayloadType,
)
from backend import util

from back.settings import LOGGING


logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case  # type: ignore
async def resolve_project_mutation(
        obj: Any,
        info: GraphQLResolveInfo,
        **parameters: Any) -> Any:
    """Wrap project mutations."""
    field = util.camelcase_to_snakecase(info.field_name)
    resolver_func = getattr(sys.modules[__name__], f'_do_{field}')
    return await resolver_func(obj, info, **parameters)


@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def _do_remove_tag(
        _: Any,
        info: GraphQLResolveInfo,
        project_name: str,
        tag: str) -> SimpleProjectPayloadType:
    """Resolve remove_tag mutation."""
    success = False
    project_name = project_name.lower()
    group_loader = info.context.loaders['group']
    if await project_domain.is_alive(project_name):
        project_attrs = await group_loader.load(project_name)
        project_tags = {'tag': project_attrs['tags']}
        cast(Set[str], project_tags.get('tag')).remove(tag)
        if project_tags.get('tag') == set():
            project_tags['tag'] = None
        tag_deleted = await project_domain.update(
            project_name, project_tags
        )
        if tag_deleted:
            success = True
        else:
            LOGGER.error('Couldn\'t remove a tag', extra={'extra': locals()})
    if success:
        util.queue_cache_invalidation(f'tags*{project_name}')
        group_loader.clear(project_name)
        util.cloudwatch_log(
            info.context,
            ('Security: Removed tag from '
             f'{project_name} project successfully')  # pragma: no cover
        )
    else:
        util.cloudwatch_log(
            info.context,
            ('Security: Attempted to remove '
             f'tag in {project_name} project')  # pragma: no cover
        )
    project = await group_loader.load(project_name)
    return SimpleProjectPayloadType(success=success, project=project)
