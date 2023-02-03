from api.mutations import (
    GrantStakeholderAccessPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from contextlib import (
    suppress,
)
from custom_exceptions import (
    InvalidRoleProvided,
    StakeholderHasOrganizationAccess,
    StakeholderNotFound,
)
from dataloaders import (
    Dataloaders,
)
from db_model.organization_access.enums import (
    OrganizationInvitiationState,
)
from db_model.organization_access.types import (
    OrganizationAccessRequest,
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
    organization_access as org_access_utils,
)
from newutils.utils import (
    map_roles,
)
from organizations import (
    domain as orgs_domain,
)
from sessions import (
    domain as sessions_domain,
)

# Constants
LOGGER = logging.getLogger(__name__)


@convert_kwargs_to_snake_case
@enforce_organization_level_auth_async
async def mutate(
    _: None, info: GraphQLResolveInfo, **parameters: dict
) -> GrantStakeholderAccessPayload:
    loaders: Dataloaders = info.context.loaders
    organization_id = str(parameters.get("organization_id"))
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    organization_name = organization.name
    requester_data = await sessions_domain.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    stakeholder_email = str(parameters.get("user_email")).lower().strip()
    stakeholder_role: str = map_roles(str(parameters.get("role")).lower())

    if organization_access := await loaders.organization_access.load(
        OrganizationAccessRequest(
            organization_id=organization_id, email=stakeholder_email
        )
    ):
        if organization_access.has_access:
            raise StakeholderHasOrganizationAccess()

        with suppress(StakeholderNotFound):
            stakeholder: Stakeholder = await loaders.stakeholder.load(
                stakeholder_email
            )
            invitation_state = org_access_utils.format_invitation_state(
                invitation=organization_access.invitation,
                is_registered=stakeholder.is_registered,
            )
            if invitation_state == OrganizationInvitiationState.REGISTERED:
                raise StakeholderHasOrganizationAccess()

        # Too soon to send another email invitation to the same stakeholder
        if organization_access.expiration_time:
            validate_new_invitation_time_limit(
                organization_access.expiration_time
            )

    allowed_roles_to_grant = (
        await authz.get_organization_level_roles_a_user_can_grant(
            loaders=loaders,
            organization_id=organization_id,
            requester_email=requester_email,
        )
    )
    if stakeholder_role in allowed_roles_to_grant:
        await orgs_domain.invite_to_organization(
            loaders=loaders,
            email=stakeholder_email,
            role=stakeholder_role,
            organization_name=organization_name,
            modified_by=requester_email,
        )
    else:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "new_stakeholder_role": stakeholder_role,
                    "organization_name": organization_name,
                    "requester_email": stakeholder_email,
                }
            },
        )
        raise InvalidRoleProvided(role=stakeholder_role)

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {stakeholder_email} was granted access "
        f"to organization {organization_name} with role {stakeholder_role} "
        f"by stakeholder {requester_email}",
    )

    return GrantStakeholderAccessPayload(
        success=True,
        granted_stakeholder=Stakeholder(
            email=stakeholder_email,
        ),
    )
