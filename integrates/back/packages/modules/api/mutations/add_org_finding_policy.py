from typing import Dict

from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

from custom_types import SimplePayload
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations_finding_policies import domain as policies_domain


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    finding_name: str,
    organization_name: str,
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]

    await policies_domain.add_finding_policy(
        finding_name=finding_name.strip(),
        org_name=organization_name,
        user_email=user_email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added a org finding policy in {organization_name}",
    )

    return SimplePayload(success=True)
