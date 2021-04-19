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
)
from backend.typing import SimplePayload
from roots import domain as roots_domain


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    await roots_domain.activate_root(
        context=info.context.loaders,
        group_name=kwargs['group_name'],
        root_id=kwargs['id'],
        user_email=user_email
    )

    return SimplePayload(success=True)
