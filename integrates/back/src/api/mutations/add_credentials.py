from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from db_model.enums import (
    CredentialType,
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
)
from organizations.types import (
    CredentialAttributesToAdd,
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
    organization_id: str,
    credentials: dict[str, str],
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    await orgs_domain.add_credentials(
        loaders,
        CredentialAttributesToAdd(
            name=credentials["name"],
            key=credentials.get("key"),
            token=credentials.get("token"),
            type=CredentialType[credentials["type"]],
            user=credentials.get("user"),
            password=credentials.get("password"),
        ),
        organization_id,
        user_email,
    )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added credentials to {organization_id} successfully",
    )

    return SimplePayload(success=True)
