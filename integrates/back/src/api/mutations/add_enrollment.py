from ariadne import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    concurrent_decorators,
    require_corporate_email,
    require_login,
)
from enrollment import (
    domain as enrollment_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    stakeholders as stakeholders_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_corporate_email,
    require_login,
)
async def mutate(
    _: Any,
    info: GraphQLResolveInfo,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]

    await enrollment_domain.add_enrollment(
        loaders=loaders,
        user_email=user_email,
        full_name=stakeholders_utils.get_full_name(user_data),
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Created enrollment user {user_email} successfully",
    )

    return SimplePayload(success=True)
