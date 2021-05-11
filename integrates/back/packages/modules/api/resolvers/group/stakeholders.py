
from functools import partial
from typing import (
    Dict,
    List,
    cast,
)

from graphql.type.definition import GraphQLResolveInfo

from custom_types import (
    Project as GroupType,
    Stakeholder as StakeholderType,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
)
from newutils import token as token_utils
from redis_cluster.operations import redis_get_or_set_entity_attr
from users import domain as users_domain


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_integrates,
)
async def resolve(
    parent: GroupType,
    info: GraphQLResolveInfo,
    **kwargs: None
) -> List[StakeholderType]:
    response: List[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity='group',
        attr='stakeholders',
        name=cast(str, parent['name'])
    )
    return response


async def resolve_no_cache(
    parent: GroupType,
    info: GraphQLResolveInfo,
    **_kwargs: None
) -> List[StakeholderType]:
    group_name: str = cast(str, parent['name'])

    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data['user_email']

    if users_domain.is_fluid_staff(user_email):
        group_stakeholders_loader = info.context.loaders.group_stakeholders
    else:
        group_stakeholders_loader = info.context.loaders.group_stakeholders_nf
    return cast(
        List[StakeholderType],
        await group_stakeholders_loader.load(group_name)
    )
