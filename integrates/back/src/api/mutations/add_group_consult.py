# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from aioextensions import (
    schedule,
)
from api.mutations import (
    AddConsultPayload,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.group_comments.types import (
    GroupComment,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
    require_squad,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from group_access.domain import (
    get_stakeholders_subscribed_to_consult,
)
from group_comments import (
    domain as group_comments_domain,
)
from mailer import (
    groups as groups_mail,
)
from newutils import (
    datetime as datetime_utils,
    logs as logs_utils,
    token as token_utils,
    validations as validations_utils,
)
import time
from typing import (
    Any,
)


async def send_group_consult_mail(
    *,
    loaders: Dataloaders,
    comment_data: GroupComment,
    user_email: str,
    group_name: str,
) -> None:
    await groups_mail.send_mail_comment(
        loaders=loaders,
        comment_data=comment_data,
        user_mail=user_email,
        recipients=await get_stakeholders_subscribed_to_consult(
            loaders=loaders,
            group_name=group_name,
            comment_type="group",
        ),
        group_name=group_name,
    )


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_squad,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str, **parameters: Any
) -> AddConsultPayload:
    loaders: Dataloaders = info.context.loaders
    validations_utils.validate_fields([parameters["content"]])
    group_name = group_name.lower()
    user_info = await token_utils.get_jwt_content(info.context)
    user_email = user_info["user_email"]
    current_time = datetime_utils.get_as_utc_iso_format(
        datetime_utils.get_now()
    )
    comment_id = int(round(time.time() * 1000))
    content = parameters["content"]
    comment_data = GroupComment(
        group_name=group_name,
        id=str(comment_id),
        content=content,
        creation_date=current_time,
        full_name=str.join(
            " ", [user_info["first_name"], user_info["last_name"]]
        ),
        parent_id=str(parameters.get("parent_comment")),
        email=user_email,
    )
    await group_comments_domain.add_comment(
        loaders, group_name, user_email, comment_data
    )
    if content.strip() not in {"#external", "#internal"}:
        schedule(
            send_group_consult_mail(
                loaders=loaders,
                comment_data=comment_data,
                user_email=user_email,
                group_name=group_name,
            )
        )

    logs_utils.cloudwatch_log(
        info.context,
        f"Security: Added comment to {group_name} group successfully",
    )

    return AddConsultPayload(success=True, comment_id=str(comment_id))
