from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
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
import json
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


@MUTATION.field("removeCredentials")
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
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]
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
