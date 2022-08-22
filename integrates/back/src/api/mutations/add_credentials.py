from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidParameter,
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
    validations as validation_utils,
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
    if "name" not in credentials:
        raise InvalidParameter("name")
    if "type" not in credentials:
        raise InvalidParameter("type")

    name: str = credentials["name"]
    validation_utils.validate_space_field(name)

    await orgs_domain.add_credentials(
        loaders,
        CredentialAttributesToAdd(
            name=name,
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
        "Security: Added credentials to organization"
        f" {organization_id} successfully",
    )

    return SimplePayload(success=True)
