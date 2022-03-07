from aioextensions import (
    collect,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups import (
    domain as groups_domain,
)
from typing import (
    Tuple,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def resolve(
    _parent: None, info: GraphQLResolveInfo, **kwargs: str
) -> Tuple[Group, ...]:
    user_email: str = kwargs["user_email"]
    active, inactive = await collect(
        [
            groups_domain.get_groups_by_user(user_email),
            groups_domain.get_groups_by_user(user_email, active=False),
        ]
    )
    user_groups = active + inactive

    loaders: Dataloaders = info.context.loaders
    groups: Tuple[Group, ...] = await loaders.group_typed.load_many(
        user_groups
    )
    return groups_domain.filter_active_groups_new(groups)
