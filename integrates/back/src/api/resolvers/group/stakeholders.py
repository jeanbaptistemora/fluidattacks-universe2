from custom_types import (
    Stakeholder as StakeholderType,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
)
from functools import (
    partial,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    token as token_utils,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from typing import (
    Any,
    Dict,
    List,
    Union,
)
from users import (
    domain as users_domain,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> List[StakeholderType]:
    user_data: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    exclude_fluid_staff = not users_domain.is_fluid_staff(user_email)
    response: List[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="stakeholders",
        name=parent["name"] if isinstance(parent, dict) else parent.name,
    )
    if exclude_fluid_staff:
        response = [
            user
            for user in response
            if not users_domain.is_fluid_staff(user["email"])
        ]
    return response


async def resolve_no_cache(
    parent: Union[Group, Dict[str, Any]],
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> List[StakeholderType]:
    group_name: str = (
        parent["name"] if isinstance(parent, dict) else parent.name
    )
    group_stakeholders_loader = info.context.loaders.group_stakeholders
    return await group_stakeholders_loader.load(group_name)
