from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    StakeholderNotFound,
)
from custom_types import (
    UpdateStakeholderPayload,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
    require_organization_access,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
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
    Any,
)

logging.config.dictConfig(LOGGING)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_organization_access,
    enforce_organization_level_auth_async,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **parameters: Any
) -> UpdateStakeholderPayload:
    success: bool = False

    organization_id: str = str(parameters.get("organization_id"))
    organization_name: str = await orgs_domain.get_name_by_id(organization_id)
    requester_data = await token_utils.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    user_email: str = str(parameters.get("user_email"))
    new_role: str = map_roles(str(parameters.get("role")).lower())

    organization_access = await orgs_dal.get_access_by_url_token(
        organization_id, user_email
    )
    # Validate role requirements before changing anything
    validate_role_fluid_reqs(user_email, new_role)
    if organization_access:
        invitation = organization_access.get("invitation")
        if invitation:
            success = await orgs_domain.update_invited_stakeholder(
                user_email, invitation, organization_id, new_role
            )
            if invitation["is_used"]:
                await authz.grant_organization_level_role(
                    user_email, organization_id, new_role
                )
        else:
            # For some users without invitation
            if await authz.grant_organization_level_role(
                user_email, organization_id, new_role
            ):
                success = True
            else:
                LOGGER.error(
                    "Couldn't update stakeholder role",
                    extra={"extra": info.context},
                )
    else:
        raise StakeholderNotFound()

    if success:
        await redis_del_by_deps(
            "update_organization_stakeholder", organization_id=organization_id
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} modified "
            f"information from the stakeholder {user_email} "
            f"in the organization {organization_name}",
        )
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} attempted to modify "
            f"information from stakeholder {user_email} in organization "
            f"{organization_name}",
        )
    return UpdateStakeholderPayload(
        success=success, modified_stakeholder=dict(email=user_email)
    )
