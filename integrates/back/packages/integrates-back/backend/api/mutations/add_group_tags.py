# Standard library
from typing import (
    Any,
    List
)

# Third party libraries
from ariadne import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.dal.helpers.redis import (
    redis_del_by_deps_soon,
)
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_integrates
)
from backend.typing import SimpleProjectPayload as SimpleProjectPayloadType
from groups import domain as groups_domain
from newutils.groups import update_tags


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
    tags: List[str]
) -> SimpleProjectPayloadType:
    success = False
    group_name = project_name.lower()
    group_loader = info.context.loaders.group
    if await groups_domain.is_alive(group_name):
        if await groups_domain.validate_group_tags(group_name, tags):
            project_attrs = await group_loader.load(group_name)
            group_tags = {'tag': project_attrs['tags']}
            success = await update_tags(
                group_name,
                group_tags,
                tags
            )
        else:
            util.cloudwatch_log(
                info.context,
                f'Security: Attempted to add tags without allowed structure'
            )
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to add tags without the allowed validations'
        )
    if success:
        group_loader.clear(group_name)
        info.context.loaders.group_all.clear(group_name)
        redis_del_by_deps_soon('add_group_tags', group_name=project_name)
        util.cloudwatch_log(
            info.context,
            f'Security: Added tag to {group_name} group successfully'
        )

    project = await group_loader.load(group_name)
    return SimpleProjectPayloadType(success=success, project=project)
