# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

from api import (
    APP_EXCEPTIONS,
)
from api.mutations import (
    SimplePayload,
)
from ariadne.utils import (
    convert_kwargs_to_snake_case,
)
from decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
    require_login,
)
from findings import (
    domain as findings_domain,
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
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
    require_finding_access,
)
async def mutate(
    _: None, info: GraphQLResolveInfo, **kwargs: Any
) -> SimplePayload:
    try:
        file: UploadFile = kwargs["file"]
        finding_id: str = kwargs["finding_id"]
        evidence_id: str = kwargs["evidence_id"]
        await findings_domain.update_evidence(
            info.context.loaders, finding_id, evidence_id, file
        )
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Updated evidence in finding {finding_id} successfully",
        )
    except APP_EXCEPTIONS:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to update evidence in finding {finding_id}",
        )
        raise

    return SimplePayload(success=True)
