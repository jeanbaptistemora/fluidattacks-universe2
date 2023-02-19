from .payloads.types import (
    AddStakeholderPayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_exceptions import (
    InvalidRoleProvided,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    enforce_user_level_auth_async,
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
import logging
import logging.config
from newutils import (
    logs as logs_utils,
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

LOGGER = logging.getLogger(__name__)


@MUTATION.field("addStakeholder")
@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_user_level_auth_async,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    email: str,
    role: str,
) -> AddStakeholderPayload:
    loaders: Dataloaders = info.context.loaders
    email = email.lower().strip()
    role = map_roles(role)
    user_data = await sessions_domain.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    allowed_roles_to_grant = await authz.get_user_level_roles_a_user_can_grant(
        loaders=loaders,
        requester_email=user_email,
    )
    if role not in allowed_roles_to_grant:
        LOGGER.error(
            "Invalid role provided",
            extra={
                "extra": {
                    "email": email,
                    "requester_email": user_email,
                    "role": role,
                }
            },
        )
        raise InvalidRoleProvided(role=role)

    await orgs_domain.add_without_group(
        email=email,
        role=role,
    )
    logs_utils.cloudwatch_log(
        info.context, f"Security: Added stakeholder {email}"
    )

    return AddStakeholderPayload(success=True, email=email)
