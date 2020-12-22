# Standard
from typing import Any, Optional

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from starlette.datastructures import UploadFile
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.domain import event as event_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    project_name: str,
    image: Optional[UploadFile] = None,
    file: Optional[UploadFile] = None,
    **kwargs: Any
) -> SimplePayload:
    """Resolve create_event mutation."""
    user_info = await util.get_jwt_content(info.context)
    analyst_email = user_info['user_email']
    success = await event_domain.create_event(
        analyst_email,
        project_name.lower(),
        file,
        image,
        **kwargs
    )
    if success:
        util.cloudwatch_log(
            info.context,
            f'Security: Created event in {project_name} project successfully'
        )
        util.queue_cache_invalidation(project_name)

    return SimplePayload(success=success)
