from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from batch.dal import (
    put_action,
)
from custom_types import (
    SimplePayload,
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
    token as token_utils,
)
from organizations_finding_policies import (
    domain as policies_domain,
)
from typing import (
    Dict,
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
    status: str,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await policies_domain.handle_finding_policy_acceptance(
        finding_policy_id=finding_policy_id,
        org_name=organization_name,
        status=status,
        user_email=user_email,
    )

    if status == "APPROVED":
        await put_action(
            action_name="handle_finding_policy",
            entity=finding_policy_id,
            subject=user_email,
            additional_info=organization_name,
        )

    return SimplePayload(success=True)
