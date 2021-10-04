from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_login,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from typing import (
    cast,
    Optional,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
)
async def resolve(
    parent: Group,
    __: GraphQLResolveInfo,
) -> Optional[str]:
    # pylint: disable=unsubscriptable-object
    group_name: str = cast(str, parent["name"])
    token: Optional[str] = await forces_domain.get_token(group_name)
    return token
