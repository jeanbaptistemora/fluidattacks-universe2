# Standard
from typing import Any, Dict

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    rename_kwargs,
    require_login,
)
from backend.domain import root as root_domain
from backend.typing import SimplePayload


@convert_kwargs_to_snake_case  # type: ignore
@rename_kwargs({'id': 'root_id'})
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
@rename_kwargs({'root_id': 'id'})
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    await root_domain.update_root_state(
        user_email,
        kwargs['id'],
        kwargs['state']
    )

    return SimplePayload(success=True)
