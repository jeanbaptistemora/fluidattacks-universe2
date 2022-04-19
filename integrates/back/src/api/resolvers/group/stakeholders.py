from custom_types import (
    Stakeholder as StakeholderType,
)
from dataloaders import (
    Dataloaders,
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
from users import (
    domain as users_domain,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> list[StakeholderType]:
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    exclude_fluid_staff = not users_domain.is_fluid_staff(user_email)
    response: list[StakeholderType] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="stakeholders",
        name=parent.name,
    )
    if exclude_fluid_staff:
        response = [
            user
            for user in response
            if not users_domain.is_fluid_staff(str(user["email"]))
        ]
    return response


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[StakeholderType]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    return await loaders.group_stakeholders.load(group_name)
