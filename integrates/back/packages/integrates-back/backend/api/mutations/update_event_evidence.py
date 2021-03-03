# Standard
# None

# Third party
from ariadne.utils import convert_kwargs_to_snake_case
from graphql.type.definition import GraphQLResolveInfo
from starlette.datastructures import UploadFile

# Local
from backend.decorators import (
    concurrent_decorators,
    enforce_group_level_auth_async,
    require_integrates,
    require_login,
)
from backend.typing import SimplePayload
from events import domain as events_domain
from newutils.datetime import get_now


@convert_kwargs_to_snake_case  # type: ignore
@concurrent_decorators(
    require_login,
    enforce_group_level_auth_async,
    require_integrates,
)
async def mutate(
    _parent: None,
    info: GraphQLResolveInfo,
    event_id: str,
    evidence_type: str,
    file: UploadFile
) -> SimplePayload:
    success = False
    if await events_domain.validate_evidence(evidence_type, file):
        success = await events_domain.update_evidence(
            event_id,
            evidence_type,
            file,
            get_now(),
        )
        info.context.loaders.event.clear(event_id)

    return SimplePayload(success=success)
