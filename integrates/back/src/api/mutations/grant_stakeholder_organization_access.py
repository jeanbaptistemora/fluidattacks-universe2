from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from context import (
    FI_DEFAULT_ORG,
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
from groups import (
    domain as groups_domain,
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
    Dict,
)
from users import (
    domain as users_domain,
)


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

    user_added = await orgs_domain.add_user(
        organization_id, user_email, user_role
    )

    user_created = False
    user_exists = bool(await users_domain.get_data(user_email, "email"))
    if not user_exists:
        user_created = await groups_domain.add_without_group(
            user_email,
            "customer",
            should_add_default_org=(
                FI_DEFAULT_ORG.lower() == organization_name.lower()
            ),
        )
    success = user_added and any([user_created, user_exists])

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
