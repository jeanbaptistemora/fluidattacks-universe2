
from typing import (
    Any,
    Dict,
)

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from newutils import token as token_utils
from roots import domain as roots_domain


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    await roots_domain.update_root_state(
        info.context.loaders,
        user_email,
        kwargs['group_name'],
        kwargs['id'],
        kwargs['state']
    )

    return SimplePayload(success=True)
