from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from authz.validations import (
    validate_role_fluid_reqs,
)
from custom_exceptions import (
    UserNotInOrganization,
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
from users import (
    domain as users_domain,
)


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
    new_phone_number: str = parameters.get("phone_number", "")

    # Validate role requirements before changing anything
    validate_role_fluid_reqs(user_email, new_role)
    if not await orgs_domain.has_user_access(organization_id, user_email):
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Stakeholder {requester_email} attempted to edit "
            f"information from a not existent stakeholder {user_email} "
            f"in organization {organization_name}",
        )
        raise UserNotInOrganization()

    success = await orgs_domain.add_user(organization_id, user_email, new_role)
    if new_phone_number:
        success = await users_domain.update_user_information(
            info.context,
            {
                "email": user_email,
                "phone_number": new_phone_number,
                "responsibility": "",
            },
            "",
        )

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
