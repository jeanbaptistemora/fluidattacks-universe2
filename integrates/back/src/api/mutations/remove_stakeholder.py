# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload as SimplePayloadType,
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
from newutils import (
    token as token_utils,
)
from remove_stakeholder.domain import (
    confirm_deletion_mail,
    get_confirm_deletion,
)


@require_login
async def mutate(
    _: None,
    info: GraphQLResolveInfo,
) -> SimplePayloadType:
    loaders: Dataloaders = info.context.loaders
    stakeholder_info = await token_utils.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    deletion = await get_confirm_deletion(
        loaders=loaders, email=stakeholder_email
    )
    if deletion and deletion.expiration_time:
        validate_new_invitation_time_limit(deletion.expiration_time)
    await confirm_deletion_mail(loaders=loaders, email=stakeholder_email)

    return SimplePayloadType(success=True)
