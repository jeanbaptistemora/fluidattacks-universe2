from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations import (
    domain as orgs_domain,
    validations as orgs_validations,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    credentials_id: str,
    organization_id: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    await orgs_validations.validate_stakeholder_is_credentials_owner(
        loaders=loaders,
        credentials_id=credentials_id,
        organization_id=organization_id,
        stakeholder=user_email,
    )
    await orgs_domain.remove_credentials(
        loaders=loaders,
        organization_id=organization_id,
        credentials_id=credentials_id,
        modified_by=user_email,
    )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Removed credentials from {organization_id} successfully",
    )

    return SimplePayload(success=True)
