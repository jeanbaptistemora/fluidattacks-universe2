# Standard
from typing import (
    Any,
    Dict,
)

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
    require_drills_white
)
from backend.typing import SimplePayload
from roots import domain as roots_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_drills_white
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    await roots_domain.update_git_environments_legacy(
        user_email,
        kwargs['group_name'],
        kwargs['id'],
        kwargs['environment_urls']
    )
    util.cloudwatch_log(
        info.context,
        f'Security: Updated git envs for root {kwargs["id"]}'
    )

    return SimplePayload(success=True)
