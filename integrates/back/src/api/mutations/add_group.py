from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from custom_types import (
    SimplePayload,
)
from db_model.groups.enums import (
    GroupLanguage,
    GroupService,
    GroupSubscriptionType,
)
from decorators import (
    concurrent_decorators,
    enforce_organization_level_auth_async,
    require_login,
)
from forces import (
    domain as forces_domain,
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
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_organization_level_auth_async,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
    description: str,
    organization_name: str,
    subscription: str = "continuous",
    language: str = "en",
    **kwargs: Any,
) -> SimplePayload:
    group_name: str = str(kwargs["group_name"]).lower()
    has_squad: bool = kwargs.get("has_squad", False)
    has_machine: bool = kwargs.get("has_machine", False)
    subscription_type = GroupSubscriptionType[subscription.upper()]
    if kwargs.get("service"):
        service = GroupService[str(kwargs["service"]).upper()]
    else:
        service = (
            GroupService.WHITE
            if subscription_type == GroupSubscriptionType.CONTINUOUS
            else GroupService.BLACK
        )
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    user_role = await authz.get_user_level_role(user_email)

    await groups_domain.add_group(
        description=description,
        group_name=group_name,
        has_machine=has_machine,
        has_squad=has_squad,
        language=GroupLanguage[language.upper()],
        organization_name=organization_name,
        service=service,
        subscription=subscription_type,
        user_email=user_email,
        user_role=user_role,
    )
    await forces_domain.add_forces_user(info, group_name)
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Created group {group_name} successfully",
    )

    return SimplePayload(success=True)
