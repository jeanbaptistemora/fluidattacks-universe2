from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.stakeholders.types import (
    Stakeholder,
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
from newutils.stakeholders import (
    format_stakeholder,
)
from redis_cluster.operations import (
    redis_get_or_set_entity_attr,
)
from stakeholders import (
    domain as stakeholders_domain,
)
from typing import (
    Any,
    Dict,
)


@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **kwargs: None,
) -> list[Stakeholder]:
    user_data: dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_data["user_email"]
    exclude_fluid_staff = not stakeholders_domain.is_fluid_staff(user_email)
    response: list[Dict[str, Any]] = await redis_get_or_set_entity_attr(
        partial(resolve_no_cache, parent, info, **kwargs),
        entity="group",
        attr="stakeholders",
        name=parent.name,
    )
    stakeholders: list[Stakeholder] = [
        format_stakeholder(item_legacy=stakeholder, item_vms=None)
        for stakeholder in response
    ]
    if exclude_fluid_staff:
        stakeholders = [
            stakeholder
            for stakeholder in stakeholders
            if not stakeholders_domain.is_fluid_staff(stakeholder.email)
        ]
    return stakeholders


async def resolve_no_cache(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Dict[str, Any]]:
    loaders: Dataloaders = info.context.loaders
    group_name: str = parent.name
    return await loaders.group_stakeholders.load(group_name)
