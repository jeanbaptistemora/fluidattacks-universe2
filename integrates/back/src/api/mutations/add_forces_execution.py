# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    enforce_group_level_auth_async,
)
from forces import (
    domain as forces_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)
from starlette.datastructures import (
    UploadFile,
)
from typing import (
    Any,
    Optional,
)


@convert_kwargs_to_snake_case
@enforce_group_level_auth_async
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    group_name: str,
    log: Optional[UploadFile] = None,
    **parameters: Any,
) -> SimplePayload:
    await forces_domain.add_forces_execution(
        group_name=group_name, log=log, **parameters
    )
    logs_utils.cloudwatch_log(
        info.context,
        (
            f"Security: Created forces execution in {group_name} "
            "group successfully"
        ),
    )
    return SimplePayload(success=True)
