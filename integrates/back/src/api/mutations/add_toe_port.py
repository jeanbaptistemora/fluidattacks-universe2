# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload as SimplePayloadType,
)
from ariadne import (
    convert_kwargs_to_snake_case,
)
from dataloaders import (
    Dataloaders,
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
from newutils import (
    logs as logs_utils,
    validations as validations_utils,
)
from sessions import (
    domain as sessions_domain,
)
from toe.ports import (
    domain as toe_ports_domain,
)
from toe.ports.types import (
    ToePortAttributesToAdd,
)
from typing import (
    Any,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    address: str,
    port: int,
    group_name: str,
    root_id: str,
    **_kwargs: Any,
) -> SimplePayloadType:
    try:
        loaders: Dataloaders = info.context.loaders
        user_data = await sessions_domain.get_jwt_content(info.context)
        user_email = user_data["user_email"]
        validations_utils.validate_fields([address])
        await toe_ports_domain.add(
            loaders=loaders,
            group_name=group_name,
            address=address,
            port=str(port),
            root_id=root_id,
            attributes=ToePortAttributesToAdd(
                be_present=True,
                has_vulnerabilities=False,
                seen_first_time_by=user_email,
            ),
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Added toe port in group {group_name} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Tried to add toe port in group {group_name}",
        )
        raise

    return SimplePayloadType(success=True)