from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_exceptions import (
    InvalidGitCredentials,
    InvalidParameter,
)
from dataloaders import (
    Dataloaders,
)
from db_model.credentials.types import (
    CredentialsRequest,
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
)
from newutils.validations import (
    validate_space_field,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.types import (
    CredentialAttributesToUpdate,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("updateCredentials")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    organization_id: str,
    credentials_id: str,
    credentials: dict[str, str],
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    is_pat: bool = bool(credentials.get("is_pat", False))
    if is_pat:
        if "azure_organization" not in credentials:
            raise InvalidParameter("azure_organization")
        validate_space_field(credentials["azure_organization"])
    if not is_pat and "azure_organization" in credentials:
        raise InvalidParameter("azure_organization")

    current_credentials = await loaders.credentials.load(
        CredentialsRequest(
            id=credentials_id,
            organization_id=organization_id,
        )
    )
    if current_credentials is None:
        raise InvalidGitCredentials()

    if current_credentials.state.type is CredentialType.OAUTH:
        raise InvalidParameter("type")
    await orgs_domain.update_credentials(
        loaders,
        CredentialAttributesToUpdate(
            name=credentials.get("name"),
            key=credentials.get("key"),
            token=credentials.get("token"),
            type=CredentialType[credentials["type"]]
            if "type" in credentials
            else None,
            user=credentials.get("user"),
            password=credentials.get("password"),
            is_pat=is_pat,
            azure_organization=credentials["azure_organization"]
            if is_pat
            else None,
        ),
        credentials_id,
        organization_id,
        user_email,
    )

    logs_utils.cloudwatch_log(
        info.context,
        "Security: Updated credentials in organization"
        f" {organization_id} successfully",
    )

    return SimplePayload(success=True)
