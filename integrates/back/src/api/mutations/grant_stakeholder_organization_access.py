from api.mutations import (
    GrantStakeholderAccessPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    StakeholderHasOrganizationAccess,
    StakeholderNotInOrganization,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organization_access.types import (
    OrganizationAccess,
)
from db_model.organizations.types import (
    Organization,
)
from db_model.stakeholders.types import (
    Stakeholder,
)
from decorators import (
    enforce_organization_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    validate_new_invitation_time_limit,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from newutils.utils import (
    map_roles,
)
from organizations import (
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Dict,
)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **parameters: Dict
) -> GrantStakeholderAccessPayload:
    success: bool = False

    organization_id = str(parameters.get("organization_id"))
    loaders: Dataloaders = info.context.loaders
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    organization_name = organization.name
    requester_data = await token_utils.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    user_email = str(parameters.get("user_email"))
    user_role: str = map_roles(str(parameters.get("role")).lower())

    try:
        organization_access: OrganizationAccess = (
            await loaders.organization_access.load(
                (organization_id, user_email)
            )
        )
        if organization_access.has_access:
            raise StakeholderHasOrganizationAccess()
        # Too soon to send another email invitation to the same stakeholder
        if organization_access.expiration_time:
            validate_new_invitation_time_limit(
                organization_access.expiration_time
            )

    except StakeholderNotInOrganization:
        allowed_roles_to_grant = (
            await authz.get_organization_level_roles_a_user_can_grant(
                organization_id=organization_id.lower(),
                requester_email=requester_email,
            )
        )

    if user_role in allowed_roles_to_grant:
        await orgs_domain.invite_to_organization(
            loaders,
            user_email,
            user_role,
            organization_name,
            requester_email,
        )
        success = True
    else:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "new_user_role": user_role,
                    "organization_name": organization_name,
                    "requester_email": user_email,
                }
            },
        )

    if success:
        await redis_del_by_deps(
            "grant_stakeholder_organization_access",
            organization_id=organization_id,
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {user_email} was granted access "
            f"to organization {organization_name} with role {user_role} "
            f"by stakeholder {requester_email}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} attempted to "
            f"grant stakeholder {user_email} {user_role} access to "
            f"organization {organization_name}",
        )
    return GrantStakeholderAccessPayload(
        success=success,
        granted_stakeholder=Stakeholder(
            email=user_email,
        ),
    )
