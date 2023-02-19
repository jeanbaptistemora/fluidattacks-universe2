from .payloads.types import (
    SimplePayload,
)
from .schema import (
    MUTATION,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from decorators import (
    require_login,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    analytics,
    logs as logs_utils,
)
from organizations import (
    utils as orgs_utils,
)
from roots import (
    validations as roots_validations,
)
from sessions import (
    domain as sessions_domain,
)
from typing import (
    Any,
    Dict,
)


@MUTATION.field("validateGitAccess")
@convert_kwargs_to_snake_case
@require_login
async def mutate(
    _parent: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_info: Dict[str, str] = await sessions_domain.get_jwt_content(
        info.context
    )
    user_email: str = user_info["user_email"]
    url = kwargs["url"]
    branch = kwargs["branch"]
    secret = orgs_utils.format_credentials_secret_type(kwargs["credentials"])
    stakeholder = await loaders.stakeholder.load(user_email)

    await roots_validations.validate_git_access(
        url=url, branch=branch, secret=secret, loaders=loaders
    )
    if stakeholder and not stakeholder.enrolled:
        await analytics.mixpanel_track(
            user_email,
            "AutoenrollCheckAccess",
            credential_type=kwargs["credentials"]["type"],
            url=url,
        )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: User {user_email} checked root access for "
        f"{url}@{branch}",
    )

    return SimplePayload(success=True)
