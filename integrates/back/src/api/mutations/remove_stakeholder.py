from .payloads.types import (
    SimplePayload,
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
from group_access.domain import (
    validate_new_invitation_time_limit,
)
from remove_stakeholder.domain import (
    confirm_deletion_mail,
    get_confirm_deletion,
)
from sessions import (
    domain as sessions_domain,
)


@require_login
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    stakeholder_info = await sessions_domain.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    deletion = await get_confirm_deletion(
        loaders=loaders, email=stakeholder_email
    )
    if deletion and deletion.expiration_time:
        validate_new_invitation_time_limit(deletion.expiration_time)
    await confirm_deletion_mail(loaders=loaders, email=stakeholder_email)

    return SimplePayload(success=True)
