# Standard library
from typing import Dict

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from backend.typing import SimplePayload
from organizations_finding_policies import domain as policies_domain


@convert_kwargs_to_snake_case  # type: ignore
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
    user_info: Dict[str, str] = await util.get_jwt_content(info.context)
    user_email: str = user_info['user_email']

    await policies_domain.add_finding_policy(
        finding_name=finding_name,
        org_name=organization_name,
        user_email=user_email
    )
    util.cloudwatch_log(
        info.context,
        f'Security: Added a org finding policy in {organization_name}'
    )

    return SimplePayload(success=True)
