# SPDX-FileCopyrightText: 2022 Fluid Attacks <development@fluidattacks.com>
#
# SPDX-License-Identifier: MPL-2.0

# None


from api.mutations import (
    DownloadFilePayload,
)
from ariadne.utils import (
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
from events import (
    domain as events_domain,
)
from graphql.type.definition import (
    GraphQLResolveInfo,
)
from newutils import (
    logs as logs_utils,
)


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_asm,
)
async def mutate(
    _parent: None, info: GraphQLResolveInfo, event_id: str, file_name: str
) -> DownloadFilePayload:
    loaders: Dataloaders = info.context.loaders
    success = False
    signed_url = await events_domain.get_evidence_link(
        loaders, event_id, file_name
    )
    if signed_url:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Downloaded file in event {event_id} successfully",
        )
        success = True
    else:
        logs_utils.cloudwatch_log(
            info.context,
            f"Security: Attempted to download file in event {event_id}",
        )
    return DownloadFilePayload(success=success, url=signed_url)
