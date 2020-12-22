# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo

# Local
from backend import util
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login
)
from backend.domain import event as event_domain
from backend.typing import DownloadFilePayload


@convert_kwargs_to_snake_case
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    file_name: str
) -> DownloadFilePayload:
    success = False
    signed_url = await event_domain.get_evidence_link(event_id, file_name)
    if signed_url:
        util.cloudwatch_log(
            info.context,
            f'Security: Downloaded file in event {event_id} successfully'
        )
        success = True
    else:
        util.cloudwatch_log(
            info.context,
            f'Security: Attempted to download file in event {event_id}'
        )
    return DownloadFilePayload(success=success, url=signed_url)
