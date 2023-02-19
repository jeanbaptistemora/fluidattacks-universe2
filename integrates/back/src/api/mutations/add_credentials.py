from .payloads.types import (
    SimplePayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    IntegratesBatchQueue,
    put_action,
)
from batch.enums import (
    Action,
    Product,
)
from custom_exceptions import (
    InvalidParameter,
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
import json
from newutils import (
    logs as logs_utils,
    validations as validation_utils,
)
from organizations import (
    domain as orgs_domain,
)
from organizations.types import (
    CredentialAttributesToAdd,
)
from sessions import (
    domain as sessions_domain,
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
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    is_pat: bool = bool(credentials.get("is_pat", False))
    if "name" not in credentials:
        raise InvalidParameter("name")
    if "type" not in credentials:
        raise InvalidParameter("type")
    if is_pat:
        if "azure_organization" not in credentials:
            raise InvalidParameter("azure_organization")
        validation_utils.validate_space_field(
            credentials["azure_organization"]
        )
    if not is_pat and "azure_organization" in credentials:
        raise InvalidParameter("azure_organization")

    name: str = credentials["name"]
    validation_utils.validate_space_field(name)

    credentials_id: str = await orgs_domain.add_credentials(
        loaders,
        CredentialAttributesToAdd(
            name=name,
            key=credentials.get("key"),
            token=credentials.get("token"),
            type=CredentialType[credentials["type"]],
            user=credentials.get("user"),
            password=credentials.get("password"),
            is_pat=is_pat,
            azure_organization=credentials["azure_organization"]
            if is_pat
            else None,
        ),
        organization_id,
        user_email,
    )

    logs_utils.cloudwatch_log(
        info.context,
        "Security: Added credentials to organization"
        f" {organization_id} successfully",
    )

    await put_action(
        action=Action.UPDATE_ORGANIZATION_REPOSITORIES,
        vcpus=2,
        product_name=Product.INTEGRATES,
        queue=IntegratesBatchQueue.SMALL,
        additional_info=json.dumps({"credentials_id": credentials_id}),
        entity=organization_id.lower().lstrip("org#"),
        attempt_duration_seconds=7200,
        subject="integrates@fluidattacks.com",
    )

    return SimplePayload(success=True)
