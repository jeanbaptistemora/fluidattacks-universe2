# Standard library
from typing import Dict

# Third party libraries
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local libraries
from backend.typing import SimplePayload
from dataloaders import Dataloaders
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from newutils import token as token_utils
from organizations import domain as orgs_domain
from organizations_finding_policies import domain as policies_domain


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
    user_email: str = user_info['user_email']
    loaders: Dataloaders = info.context.loaders
    org_id: str = await orgs_domain.get_id_by_name(organization_name)
    groups = await orgs_domain.get_groups(org_id)

    await policies_domain.handle_finding_policy_acceptation(
        finding_policy_id=finding_policy_id,
        loaders=loaders,
        org_name=organization_name,
        status=status,
        groups=groups,
        user_email=user_email
    )

    return SimplePayload(success=True)
