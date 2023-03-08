from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.utils import (
    format_policies_to_update,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups.domain import (
    get_group,
    update_policies,
)
from newutils import (
    logs as logs_utils,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("updateGroupPolicies")
@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    email = user_data["user_email"]
    group = await get_group(loaders, group_name.lower())
    policies_to_update = format_policies_to_update(kwargs)

    await update_policies(
        loaders=loaders,
        email=email,
        group_name=group.name,
        organization_id=group.organization_id,
        policies_to_update=policies_to_update,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {email} "
        f"updated policies for group {group.name}",
    )

    return SimplePayload(success=True)
