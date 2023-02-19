from .payloads.types import (
    SimplePayload,
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
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    organization_id = kwargs.pop("organization_id")
    organization_name = kwargs.pop("organization_name")
    policies_to_update = format_policies_to_update(kwargs)
    await orgs_domain.update_policies(
        loaders,
        organization_id,
        organization_name,
        user_email,
        policies_to_update,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: User {user_email} updated policies for organization "
        f"{organization_name} with ID {organization_id}",
    )
    return SimplePayload(success=True)
