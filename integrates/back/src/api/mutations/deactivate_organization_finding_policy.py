from .payloads.types import (
    SimplePayload,
)
from ariadne.utils import (
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
from organizations_finding_policies import (
    domain as policies_domain,
)
from sessions import (
    domain as sessions_domain,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_policy_id: str,
    organization_name: str,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info: dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]

    await policies_domain.deactivate_finding_policy(
        loaders=loaders,
        email=user_email,
        finding_policy_id=finding_policy_id,
        organization_name=organization_name,
    )

    await put_action(
        action=Action.HANDLE_FINDING_POLICY,
        entity=finding_policy_id,
        subject=user_email,
        additional_info=organization_name,
        product_name=Product.INTEGRATES,
        queue=IntegratesBatchQueue.SMALL,
    )

    return SimplePayload(success=True)
