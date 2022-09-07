# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
)
from db_model.groups.types import (
    Group,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_login,
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
from redis_cluster.operations import (
    redis_del_by_deps_soon,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, group_name: str
) -> SimplePayloadType:
    stakeholder_info = await token_utils.get_jwt_content(info.context)
    stakeholder_email = stakeholder_info["user_email"]
    loaders: Dataloaders = info.context.loaders
    await groups_domain.unsubscribe_from_group(
        loaders=loaders,
        group_name=group_name,
        email=stakeholder_email,
    )
    group: Group = await loaders.group.load(group_name)
    group_org_id = group.organization_id
    redis_del_by_deps_soon(
        "unsubscribe_from_group",
        group_name=group_name,
        organization_id=group_org_id,
    )
    msg = (
        f"Security: Unsubscribed stakeholder: {stakeholder_email} "
        f"from {group_name} group successfully"
    )
    logs_utils.cloudwatch_log(info.context, msg)

    return SimplePayloadType(success=True)
