from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
import authz
from dataloaders import (
    Dataloaders,
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
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
)


@MUTATION.field("addGroup")
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
    loaders: Dataloaders = info.context.loaders
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
    user_data = await sessions_domain.get_jwt_content(info.context)
    email = user_data["user_email"]
    granted_role = await authz.get_user_level_role(loaders, email)

    await groups_domain.add_group(
        loaders=loaders,
        description=description,
        email=email,
        granted_role=granted_role,
        group_name=group_name,
        has_machine=has_machine,
        has_squad=has_squad,
        language=GroupLanguage[language.upper()],
        organization_name=organization_name,
        service=service,
        subscription=subscription_type,
    )
    await forces_domain.add_forces_stakeholder(
        loaders=loaders, group_name=group_name, modified_by=email
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Created group {group_name} successfully",
    )

    return SimplePayload(success=True)
