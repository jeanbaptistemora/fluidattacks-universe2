from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from custom_types import (
    SimplePayload,
)
from decorators import (
    concurrent_decorators,
    require_login,
    require_service_white,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from organizations import (
    utils as orgs_utils,
)
from roots import (
    validations as roots_validations,
)
from typing import (
    Any,
    Dict,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    require_service_white,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    user_info: Dict[str, str] = await token_utils.get_jwt_content(info.context)
    user_email: str = user_info["user_email"]
    secret = orgs_utils.format_credentials_secret_type(kwargs["credentials"])
    await roots_validations.validate_git_access(
        url=kwargs["url"], branch=kwargs["branch"], secret=secret
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: User {user_email} checked root access in "
        f"{kwargs['group_name'].lower()}",
    )

    return SimplePayload(success=True)
