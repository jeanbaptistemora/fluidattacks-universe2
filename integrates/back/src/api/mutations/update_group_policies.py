# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from db_model.utils import (
    format_policies_to_update,
)
from decorators import (
    enforce_group_level_auth_async,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from groups.domain import (
    update_policies,
)
from newutils import (
    logs as logs_utils,
    token as token_utils,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    **kwargs: Any,
) -> SimplePayload:
    loaders: Dataloaders = info.context.loaders
    user_data = await token_utils.get_jwt_content(info.context)
    user_email = user_data["user_email"]
    group: Group = await loaders.group.load(group_name.lower())
    policies_to_update = format_policies_to_update(kwargs)

    await update_policies(
        group_name=group.name,
        loaders=loaders,
        organization_id=group.organization_id,
        policies_to_update=policies_to_update,
        user_email=user_email,
    )
    logs_utils.cloudwatch_log(
        info.context,
        f"Security: User {user_email} updated policies for group {group.name}",
    )

    return SimplePayload(success=True)
