# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    UpdateStakeholderPayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    StakeholderNotFound,
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
    domain as orgs_domain,
)
from redis_cluster.operations import (
    redis_del_by_deps,
)
from typing import (
    Any,
)

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
    loaders: Dataloaders = info.context.loaders
    organization_id: str = str(parameters.get("organization_id"))
    organization: Organization = await loaders.organization.load(
        organization_id
    )
    requester_data = await token_utils.get_jwt_content(info.context)
    requester_email = requester_data["user_email"]

    user_email: str = str(parameters.get("user_email"))
    new_role: str = map_roles(str(parameters.get("role")).lower())

    try:
        organization_access: OrganizationAccess = (
            await loaders.organization_access.load(
                (organization_id, user_email)
            )
        )
        # Validate role requirements before changing anything
        validate_role_fluid_reqs(user_email, new_role)
        if organization_access.invitation:
            await orgs_domain.update_invited_stakeholder(
                user_email,
                organization_access.invitation,
                organization_id,
                new_role,
            )
            if organization_access.invitation.is_used:
                await authz.grant_organization_level_role(
                    loaders, user_email, organization_id, new_role
                )
        else:
            # For some users without invitation
            await authz.grant_organization_level_role(
                loaders, user_email, organization_id, new_role
            )
    except StakeholderNotInOrganization as ex:
        raise StakeholderNotFound() from ex

    await redis_del_by_deps(
        "update_organization_stakeholder", organization_id=organization_id
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Stakeholder {requester_email} modified "
        f"information from the stakeholder {user_email} "
        f"in the organization {organization.name}",
    )

    return UpdateStakeholderPayload(
        success=True, modified_stakeholder=dict(email=user_email)
    )
