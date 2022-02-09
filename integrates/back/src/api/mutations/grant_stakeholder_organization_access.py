from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    StakeholderHasOrganizationAccess,
)
from custom_types import (
    GrantStakeholderAccessPayload,
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
    dal as orgs_dal,
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from settings import (
    LOGGING,
)
from typing import (
    Dict,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **parameters: Dict
) -> GrantStakeholderAccessPayload:
    success: bool = False

    organization_id = str(parameters.get("organization_id"))
    organization_name = await orgs_domain.get_name_by_id(organization_id)

    requester_data = await token_utils.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    user_email = str(parameters.get("user_email"))
    user_role: str = map_roles(str(parameters.get("role")).lower())

    organization_access = await orgs_dal.get_access_by_url_token(
        organization_id, user_email
    )
    if organization_access:
        # Stakeholder has already accepted the invitation
        if organization_access["has_access"]:
            raise StakeholderHasOrganizationAccess()
        # Too soon to send another email invitation to the same stakeholder
        if "expiration_time" in organization_access:
            validate_new_invitation_time_limit(
                organization_access["expiration_time"]
            )

    allowed_roles_to_grant = (
        await authz.get_organization_level_roles_a_user_can_grant(
            organization=organization_name,
            requester_email=requester_email,
        )
    )

    if user_role in allowed_roles_to_grant:
        success = await orgs_domain.invite_to_organization(
            user_email,
            user_role,
            organization_name,
            requester_email,
        )
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
        success=success, granted_stakeholder={"email": user_email}
    )
