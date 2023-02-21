from .schema import (
    GROUP,
)
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
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    get_group_stakeholders,
)
from sessions import (
    domain as sessions_domain,
)


@GROUP.field("stakeholders")
@concurrent_decorators(
    enforce_group_level_auth_async,
    require_asm,
)
async def resolve(
    parent: Group,
    info: GraphQLResolveInfo,
    **_kwargs: None,
) -> list[Stakeholder]:
    loaders: Dataloaders = info.context.loaders
    # The store is needed to resolve stakeholder's role
    request_store = sessions_domain.get_request_store(info.context)
    request_store["entity"] = "GROUP"
    request_store["group_name"] = parent.name
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    stakeholders = await get_group_stakeholders(
        loaders,
        parent.name,
        user_email,
    )

    return stakeholders
